from flask import request, session
from flask_socketio import emit
from datetime import datetime
from .extensions import socketio, db
from .models import Message, User

users = {}

@socketio.on("connect")
def handle_connect():
    print("Client connected!")

@socketio.on("user_join")
def handle_user_join(username):
    print(f"User {username} joined!")
    users[request.sid] = username
    user_id = session.get('user_id')  # Get the user_id from the session

    if user_id:
        # Emit previous messages to the joining user
        messages = Message.query.filter_by(user_id=user_id).all()
        for message in messages:
            emit("chat", {
                "username": message.username,
                "message": message.message,
                "timestamp": message.timestamp.strftime("%A, %B %d, %Y %I:%M %p")
            }, room=request.sid)

@socketio.on("new_message")
def handle_new_message(message):
    print(f"New message: {message}")
    username = users.get(request.sid)
    user_id = session.get('user_id')  # Assuming the user_id is stored in session

    if username and user_id:
        # Save message to the database
        new_message = Message(user_id=user_id, username=username, message=message, timestamp=datetime.now())
        db.session.add(new_message)
        db.session.commit()

        # Broadcast the message to all clients (optionally only to the user's room)
        emit("chat", {
            "username": username,
            "message": message,
            "timestamp": new_message.timestamp.strftime("%A, %B %d, %Y %I:%M %p")
        }, broadcast=True)

@socketio.on("disconnect")
def handle_disconnect():
    print(f"User {users.get(request.sid)} disconnected!")
    users.pop(request.sid, None)
