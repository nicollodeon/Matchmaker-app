from app import db # db created in __init__
from datetime import datetime        
from werkzeug.security import generate_password_hash, check_password_hash       # for hash functions/our passwords
from flask_login import UserMixin # class that provides functions for keeping track of log ins
from app import login
from flask import url_for
from flask_login import current_user


# data base to house our users

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    gender = db.Column(db.String(64), index=True)
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    pfp_image = db.Column(db.String(100), nullable=False, server_default='whale.png')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def avatar(self):
        return(url_for('static', filename = 'profile_pic/' + self.pfp_image))
    
    # how to print object of this class if python wants it
    def __repr__(self):
        return '<User {}, {}>'.format(self.id, self.username)
    
class Matches(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user1 = db.Column(db.Integer, db.ForeignKey('user.id'))
    user2 = db.Column(db.Integer, db.ForeignKey('user.id'))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    def __repr__(self):
        return '<Matches {}, {}>'.format(self.user1, self.user2)

class Chats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.Integer, db.ForeignKey('user.id'))
    receiver = db.Column(db.Integer, db.ForeignKey('user.id'))
    msg = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<Chats {}, {}, {}>'.format(self.sender, self.receiver, self.msg)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)

# gives login class the function it wants
# so in each page, the user id is loaded into memory
@login.user_loader
def load_user(id):
    return User.query.get(int(id))