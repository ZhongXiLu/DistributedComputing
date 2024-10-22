from flask import Blueprint, jsonify, request, g
from sqlalchemy import exc
from sqlalchemy.orm import Query
from util.verify_password import login_decorator

from util.verify_password import login_decorator
from util.send_request import send_request
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
    """
    Creates a new message.
    Notifies:
        anti-cyberbullying,
        ad
    """
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
        # Check for bad words
        r_obj = send_request('post', 'anti-cyberbullying', 'anti_cyberbullying/contains_bad_word',
                             timeout=3, json={'sentence': str(contents)},
                             auth=(g.user_id_or_token, g.password))
        response_object['anti-cyberbullying'] = r_obj.json
        if r_obj.status_code == 201:
            if r_obj.json['result']:
                response_object['message'] = f'Post contains bad words: {r_obj.json["bad_word"]}'
                return jsonify(response_object), 201

        # Update user categories for ads
        r_obj = send_request('post', 'ad', f'ads/user/{sender_id}',
                             timeout=3, json={'sentence': str(contents)},
                             auth=(g.user_id_or_token, g.password))
        response_object['ad'] = r_obj.json

        # Send notification to receiver
        try:
            response_obj = send_request('get', 'users', f'users/{sender_id}', timeout=3,
                                        auth=(g.user_id_or_token, g.password))
            response_object['users'] = response_obj.json
            username = response_obj.json['data']['username']

            send_request('post', 'notification', 'notifications', timeout=3,
                         json={'content': f'{username} has sent you a message', 'recipients': [receiver_id]},
                         auth=(g.user_id_or_token, g.password))
            response_object['notification'] = response_obj.json
        except:
            pass

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
    messages = Message.query.filter_by(receiver_id=user_id, is_read=False) \
        .order_by(Message.sender_id, Message.time_sent).all()
    return jsonify({
        'status': 'success',
        'messages': [m.to_json() for m in messages]
    }), 200
