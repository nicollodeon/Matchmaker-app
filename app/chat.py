from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_socketio import SocketIO, send, join_room, emit
from threading import Thread, Timer
from datetime import datetime
from uuid import uuid4
from app import socketio, db
from app.models import Chats, Matches, User

timers = {}
decisions = {}

@socketio.on('send_message')
def handle_send_message(data):
    recipient_username = data['recipient_username']
    message = data['message']
    # add chat record to Chats
    current_user_id = User.query.filter_by(username=current_user.username).first_or_404().id
    recipient_user_id = User.query.filter_by(username=data['recipient_username']).first_or_404().id
    chat = Chats(receiver=recipient_user_id,
                 sender=current_user_id,
                 msg=message )
    db.session.add(chat)
    db.session.commit()
    room = sorted([current_user.username, recipient_username])
    room = f"{room[0]}_{room[1]}"
    print(f"Sending message from {current_user.username} to {recipient_username} in room {room}")
    #emit('message', {'sender_username': current_user.username, 'message': message}, room=room,)
    send({'sender_username': current_user.username, 'message': message}, room=room, skip_sid=request.sid)
    # ADD DATABASE STUFF HERE

@socketio.on('join_room')
def handle_join_room(data):
    recipient_username = data['recipient_username']
    room = sorted([current_user.username, recipient_username])
    room = f"{room[0]}_{room[1]}"
    print(f"{current_user.username} joining room {room}")
    join_room(room)
    #emit('message', {'sender_username': current_user.username, 'message': f'{current_user.username} has joined the chat.'}, room=room)

@socketio.on('end_chat')
def handle_end_chat(data):
    room = sorted([current_user.username, data['recipient_username']])
    room = f"{room[0]}_{room[1]}"

    decisions[room] = decisions.get(room, [])
    decisions[room].append(data['action'])
    print("I have reached this code 0")

    if len(decisions[room]) == 1:  # This is the first decision for this room
        # Start a timer to automatically end the chat in 10 seconds
        timer = Timer(1000.0, end_chat, args=[room, 'cancel'])
        timer.start()
        timers[room] = timer
    else:  # Both users have made a decision
        # Cancel the timer
        timer = timers.pop(room)
        timer.cancel()
        print("I have reached this code 1")
        # Decide the action to take
        if 'cancel' in decisions[room]:
            action = 'end'
            print("I have reached this code 3")
        elif 'match' in decisions[room] and 'extend' not in decisions[room]:
            action = 'match'
            current_user_id = User.query.filter_by(username=current_user.username).first_or_404().id
            recipient_user_id = User.query.filter_by(username=data['recipient_username']).first_or_404().id
            match = Matches(user1=current_user_id,
                            user2=recipient_user_id,
                            timestamp=datetime.utcnow())
            db.session.add(match)
            match = Matches(user1=recipient_user_id,
                            user2=current_user_id,
                            timestamp=datetime.utcnow())
            db.session.add(match)
            db.session.commit()

            print("I have reached this code 2")
        else:
            action = 'extend'
            print("I have reached this code 4")
        emit('chat_decision', {'action': action}, room=room)
        del decisions[room]

def end_chat(room, action):
    emit('chat_decision', {'action': action}, room=room)
    # read actions, if match DB stuff here
    del decisions[room]
    del timers[room]