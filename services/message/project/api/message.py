from flask import Blueprint, jsonify, request
from sqlalchemy import exc
from sqlalchemy.orm import Query

from util.verify_password import login_decorator
from project.api.models import Message
from project import db

import requests
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()

message_blueprint = Blueprint('message', __name__, url_prefix='/message')


@message_blueprint.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })


from project import create_app
app = create_app()

@message_blueprint.route('', methods=['POST'])
@login_decorator
def create_message():
    """Create message"""
    post_data = request.get_json()
    response_object = {
        'status': 'fail',
        'message': 'Invalid payload.'
    }
    if not post_data:
        return jsonify(response_object), 400

    contents = post_data.get('contents')
    sender_id = post_data.get('sender_id')
    receiver_id = post_data.get('receiver_id')
    if contents is None or sender_id is None or receiver_id is None:
        return jsonify(response_object), 400

    try:
        db.session.add(Message(contents=contents, sender_id=sender_id, receiver_id=receiver_id))
        db.session.commit()
        response_object['status'] = 'success'
        response_object['message'] = 'message was successfully created'
        return jsonify(response_object), 201
    except Exception as e:
        db.session.rollback()
        return jsonify(response_object), 400


@message_blueprint.route('<int:user_id>/<int:correspondent_id>', defaults={'amount': None}, methods=['GET'])
@message_blueprint.route('<int:user_id>/<int:correspondent_id>/<int:amount>', methods=['GET'])
@login_decorator
def get_messages(user_id, correspondent_id, amount=None):
    """Get messages in conversation between receiver and sender sorted by timestamp"""
    q1 = Message.query.filter_by(sender_id=user_id, receiver_id=correspondent_id)
    q2 = Message.query.filter_by(sender_id=correspondent_id, receiver_id=user_id)
    q3 = q1.union(q2)  # type: Query
    q4 = q3.order_by(Message.time_sent.desc())
    messages = q4.all() if amount is None else q4.limit(amount).all()
    q1.update({Message.is_read: True}, synchronize_session=False)
    q2.update({Message.is_read: True}, synchronize_session=False)
    db.session.commit()

    return jsonify({
        'status': 'success',
        'messages': [m.to_json() for m in reversed(messages)]
    }), 200


@message_blueprint.route('<int:user_id>/unread', methods=['GET'])
@login_decorator
def get_unread(user_id):
    """Get all unread messages where the user is the receiver"""
    messages = Message.query.filter_by(receiver_id=user_id, is_read=False)\
        .order_by(Message.sender_id, Message.time_sent).all()
    return jsonify({
        'status': 'success',
        'messages': [m.to_json() for m in messages]
    }), 200

