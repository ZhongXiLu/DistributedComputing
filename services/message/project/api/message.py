from flask import Blueprint, jsonify, request
from sqlalchemy import exc
from sqlalchemy.orm import Query

from util.verify_password import verify_password
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


@message_blueprint.route('', methods=['POST'])
@auth.login_required
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
    sender_id = auth.username()
    receiver_id = post_data.get('receiver_id')
    if contents is None or receiver_id is None:
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


@message_blueprint.route('<int:correspondent_id>/<int:amount>', methods=['GET'])
@auth.login_required
def get_messages(correspondent_id, amount=None):
    """Get messages in conversation between receiver and sender sorted by timestamp"""
    q1 = Message.query.filter_by(sender_id=auth.username(), receiver_id=correspondent_id)
    q2 = Message.query.filter_by(sender_id=correspondent_id, receiver_id=auth.username())
    q3 = q1.union(q2).order_by(Message.time_sent)  # type: Query
    messages = q3.all() if amount is None else q3.limit(amount).all()
    q3.update({Message.is_read: True}, synchronize_session=False)
    db.session.commit()

    return jsonify({
        'status': 'success',
        'messages': [m.to_json() for m in messages]
    }), 200


@message_blueprint.route('unread', methods=['GET'])
@auth.login_required
def get_unread():
    """Get all unread messages where the user is the receiver"""
    messages = Message.query.filter_by(receiver_id=auth.username(), is_read=False)\
        .order_by(Message.sender_id, Message.time_sent).all()
    return jsonify({
        'status': 'success',
        'messages': [m.to_json() for m in messages]
    }), 200

