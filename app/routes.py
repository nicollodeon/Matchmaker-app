from flask import render_template, flash, redirect, url_for, request, jsonify, session
from app import app, db
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user, login_required
from flask_socketio import SocketIO, send, join_room, emit
from app.models import User, Chats, Matches
from werkzeug.urls import url_parse
from datetime import datetime
from app.forms import EditProfileForm
import secrets
import os
from sqlalchemy import or_, and_
import random

logged_in = dict()  # store user session id and their username
queued_males = {}
queued_females = {}

# the main router -> whatever request comes in direct to right program/html
# @login_required to protect routes
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title='Home')


# decorators (python), registers below functions as callback for those events
@app.route('/index/<username>', methods=['GET', 'POST'])
@login_required         # protect routes with log in required
def index(username):
    form = EditProfileForm()
    if form.validate_on_submit():
        if form.picture.data:
            current_user.pfp_image = save_picture(form.picture.data)
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        current_user.gender = form.gender.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('index', username=current_user.username))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
        form.gender.data = current_user.gender
        form.email.data = current_user.email
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('index.html', user=user, title='home', form=form)


# tells flask can send GET and POST to this function
@app.route('/login', methods=['GET', 'POST'])
def login():
    print(request.form)
    # redirected logged in people away from login page
    # current user in envr determined from user.loader
    if current_user.is_authenticated:
        # redirect forces a url change
        return redirect(url_for('index', username=current_user.username))
    print("passed")
    # LoginForm instance to be passed in
    form = LoginForm()
    # form.validate... runs all the validators, will return false for GET requests or POST data that failed the validation
    if form.validate_on_submit():
        # query database for the first equal
        user = User.query.filter_by(username=form.username.data).first()
        # if no results from query/bad password
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        # from flask-login, set it user as "logged in" so will appear in current user
        login_user(user, remember=form.remember_me.data)
        logged_in[current_user.get_id()] = user.username
        # next is a parameter in the url, can record where user comes from so after logging in can go back to page
        next_page = request.args.get('next')
        # set a default next page
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index', username=current_user.username)
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

# for record date of last visit


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

# save the file into static


def save_picture(form_picture):
    rand_hex = secrets.token_hex(8)
    # grab f ext, throw file name
    _, file_ext = os.path.splitext(form_picture.filename)
    pic_fname = rand_hex + file_ext
    pic_ospath = os.path.join(
        app.root_path, 'static/profile_pic', pic_fname)  # full path name
    print(pic_ospath)
    form_picture.save(pic_ospath)
    return (pic_fname)


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        if form.picture.data:
            current_user.pfp_image = save_picture(form.picture.data)
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        current_user.gender = form.gender.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
        form.gender.data   = form.gender.data
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)


@app.route('/logout')
def logout():
    # queued.remove(logged_in[current_user.get_id()])
    # logged_in.pop(current_user.get_id())
    logout_user()
    return redirect(url_for('home'))


@app.route('/history', defaults={'username': None})
@app.route('/history/<username>')
@login_required
def history(username):

    #left for debuggin if needed
    #     users = User.query.all()
    # for user in users:
    #     print(user)

    # matches = Matches.query.all()
    # for match in matches:
    #     print(match)

    # chats = Chats.query.all()
    # for chat in chats:
    #     print(chat)

    current_user_id = User.query.filter_by(username=current_user.username).first_or_404().id

    subquery = (
        db.session.query(Matches.user2)
        .filter(Matches.user1 == current_user_id)
        .all()
    )

    if subquery is not None:
        user2_list = [row[0] for row in subquery]   
        users = (
            db.session.query(User)
            .filter(User.id.in_(user2_list))
            .all()
        )
    else:
        users=None
    
    first_match = Matches.query.filter_by(user1=current_user_id).first()
    if first_match is None:
        print("first_match is none")
    if users is None:
        print("users is none")
    if username is None:
        print("username is none")
        if first_match is None:
            chat_of_interest = None
        else:
            chat_of_interest = Chats.query.filter(
                    or_(
                        and_(Chats.sender == current_user_id, Chats.receiver == first_match.user2),
                        and_(Chats.sender == first_match.user2, Chats.receiver == current_user_id)
                    )
                ).all()
    else:
        print("else")
        username_id = User.query.filter_by(username=username).first_or_404().id
        chat_of_interest = Chats.query.filter(
                or_(
                    and_(Chats.sender == current_user_id, Chats.receiver == username_id),
                    and_(Chats.sender == username_id, Chats.receiver == current_user_id)
                )
            ).all()
    return render_template('history.html', title='history', c_user_id=current_user_id, matchedUsers=users, chats=chat_of_interest)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index', username=current_user.username))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, gender=form.gender.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)


@login_required
@app.route('/private_chat/<recipient_username>')
# recipient_id replaced with username things?
def private_chat(recipient_username):
    recipient = User.query.filter_by(username=recipient_username).first()
    if not recipient:
        flash('User not found.', 'error')
        return redirect(url_for('index', username=current_user.username))
    else:
        # get recipient and current user data from Chats db
        chatsList = Chats.query.filter(
            or_(
                Chats.sender == current_user.username,
                Chats.receiver == recipient_username,
                and_(Chats.sender == recipient_username,
                     Chats.receiver == current_user.username)
            )
        ).all()

    return render_template('private_chat.html', recipient=recipient, chatsList=chatsList, sender=current_user.username)


@app.route('/queue', methods=['GET', 'POST'])
@login_required
def queue():
    male_user_ids = queued_males.keys()
    female_user_ids = queued_females.keys()
    all_queued_ids = list(male_user_ids) + list(female_user_ids)
    users = User.query.filter(User.id.in_(all_queued_ids)).all()
    return render_template('queue.html', users=users)


@app.route('/join_queue', methods=['POST'])
@login_required
def join_queue():
    user_id = current_user.get_id()
    user_gender = User.query.get(user_id).gender

    if user_gender == 'male':
        queued_males[user_id] = ''
    elif user_gender == 'female':
        queued_females[user_id] = ''

    return jsonify({'status': 'success'}), 200


@app.route('/check_queue_status')
@login_required
def check_queue_status():
    user_id = current_user.get_id()
    user_gender = User.query.get(user_id).gender

    in_queue = False
    chat_url = ''

    if user_gender == 'male':
        in_queue = user_id in queued_males
        chat_url = queued_males.get(user_id, '')
        # Only pair users when there is a female and this user is the first male in the queue
        if in_queue and len(queued_females) > 0 and next(iter(queued_males.keys())) == user_id:
            other_user_id = next(iter(queued_females.keys()))
            chat_url = prepare_chat(user_id, other_user_id)

    elif user_gender == 'female':
        in_queue = user_id in queued_females
        chat_url = queued_females.get(user_id, '')
        # Only pair users when there is a male and this user is the first female in the queue
        if in_queue and len(queued_males) > 0 and next(iter(queued_females.keys())) == user_id:
            other_user_id = next(iter(queued_males.keys()))
            chat_url = prepare_chat(user_id, other_user_id)

    return jsonify({'in_queue': in_queue and not chat_url, 'chat_url': chat_url}), 200



@app.route('/leave_queue', methods=['POST'])
@login_required
def leave_queue():
    user_id = current_user.get_id()
    user_gender = User.query.get(user_id).gender

    if user_gender == 'male' and user_id in queued_males:
        queued_males.pop(user_id)
    elif user_gender == 'female' and user_id in queued_females:
        queued_females.pop(user_id)

    return jsonify({'status': 'success'}), 200


def prepare_chat(user1_id, user2_id):
    user1 = User.query.get(user1_id)
    user2 = User.query.get(user2_id)
    chat_url = url_for('private_chat', recipient_username=user2.username)
    if user1.gender == 'male':
        queued_males[user1_id] = chat_url
        queued_females[user2_id] = chat_url
    else:
        queued_females[user1_id] = chat_url
        queued_males[user2_id] = chat_url
    return chat_url


if __name__ == '__main__':
    socketio.run(app, debug=True)