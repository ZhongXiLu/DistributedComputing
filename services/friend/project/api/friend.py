from flask import Blueprint, jsonify, request, g
from sqlalchemy import exc

from util.send_request import send_request
from util.verify_password import verify_password
from project.api.models import Friend
from project import db
from util.verify_password import login_decorator

import requests
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()

friend_blueprint = Blueprint('friend', __name__, url_prefix='/friend')


@friend_blueprint.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })


@friend_blueprint.route('request', methods=['POST'])
@login_decorator
def create_friend():
    """Create friend request"""
    post_data = request.get_json()
    response_object = {
        'status': 'fail',
        'message': 'Invalid payload.'
    }
    if not post_data:
        return jsonify(response_object), 400

    friend_initiator_id = post_data.get('friend_initiator_id')
    friend_acceptor_id = post_data.get('friend_acceptor_id')
    if friend_initiator_id is None or friend_acceptor_id is None:
        return jsonify(response_object), 400

    if int(friend_initiator_id) == int(friend_acceptor_id):
        response_object['message'] = 'You cannot friend yourself'
        return jsonify(response_object), 400

    try:
        if Friend.query.filter_by(friend_initiator_id=friend_acceptor_id,
                                  friend_acceptor_id=friend_initiator_id).count():
            response_object['message'] = 'Friendship already exists or is already requested'
            return jsonify(response_object), 400

        db.session.add(Friend(friend_initiator_id=friend_initiator_id, friend_acceptor_id=friend_acceptor_id))
        db.session.commit()
        response_object['status'] = 'success'
        response_object['message'] = 'friendship request was successfully created'

        try:
            response_obj = send_request('get', 'users', f'users/{friend_initiator_id}', timeout=3, auth=(g.user_id_or_token, g.password))
            response_object['users'] = response_obj.json
            username = f'User {friend_initiator_id}'
            try:
                username = response_obj.json['data']['username']
            except:
                pass

            response_obj = send_request('post', 'notification', 'notifications', timeout=3,
                                           json={'content': f'{username} has sent you a friend invite',
                                                 'recipients': [friend_acceptor_id]},
                                           auth=(g.user_id_or_token, g.password))
            response_object['notification'] = response_obj.json
        except:
            response_object['warning'] = 'failed creating a notification'

        return jsonify(response_object), 201
    except Exception as e:
        db.session.rollback()
        # response_object["what"] = str(e)
        return jsonify(response_object), 400


@friend_blueprint.route('accept', methods=['put'])
@login_decorator
def accept_friend():
    """Accept friend request"""
    put_data = request.get_json()
    response_object = {
        'status': 'fail',
        'message': 'Invalid payload.'
    }
    if not put_data:
        return jsonify(response_object), 400

    friend_initiator_id = put_data.get('friend_initiator_id')
    friend_acceptor_id = put_data.get('friend_acceptor_id')
    if friend_initiator_id is None or friend_acceptor_id is None:
        return jsonify(response_object), 400

    try:
        friend = Friend.query.filter_by(
            friend_initiator_id=friend_initiator_id, friend_acceptor_id=friend_acceptor_id).first()
        friend.is_accepted = True
        db.session.commit()
        response_object['status'] = 'success'
        response_object['message'] = 'friendship request was successfully accepted'

        # Get name of acceptor
        r_obj = send_request('get', 'users', f'users/{friend_acceptor_id}', timeout=3,
                             auth=(g.user_id_or_token, g.password))
        try:
            friend_acceptor_name = r_obj.json['data']['username']
        except:
            friend_acceptor_name = f'User {friend_initiator_id}'

        # Send notification to initiator
        r_obj = send_request('post', 'notification', 'notifications', timeout=3,
                             json={'content': f'{friend_acceptor_name} has sent you a friend invite',
                                   'recipients': [friend_initiator_id]},
                             auth=(g.user_id_or_token, g.password))
        response_object['notification'] = r_obj.json

        return jsonify(response_object), 200
    except Exception as e:
        db.session.rollback()
        # response_object["what"] = str(e)
        return jsonify(response_object), 400


@friend_blueprint.route('/<friend1_id>/<friend2_id>', methods=['DELETE'])
@login_decorator
def delete_friend(friend1_id, friend2_id):
    """Delete a friendship"""
    response_object = {
        'status': 'fail',
        # 'message': 'Invalid payload.'
    }
    try:
        q1 = Friend.query.filter_by(friend_initiator_id=friend1_id, friend_acceptor_id=friend2_id)
        q2 = Friend.query.filter_by(friend_initiator_id=friend2_id, friend_acceptor_id=friend1_id)
        friend = q1.union(q2).first()
        if friend:
            db.session.delete(friend)
            db.session.commit()
            response_object['status'] = 'success'
            response_object['message'] = f'{friend1_id} and {friend2_id} are no longer friends.'
            return jsonify(response_object), 200
    except exc.IntegrityError:
        db.session.rollback()
    return jsonify(response_object), 400


@friend_blueprint.route('/<user_id>/requests', methods=['GET'])
def get_friend_requests(user_id):
    """Get all friends requests sent to the user"""
    friend_requests = Friend.query.filter_by(friend_acceptor_id=user_id, is_accepted=False)
    return jsonify({
        'status': 'success',
        'friends_requests': [x.friend_initiator_id for x in friend_requests],
    })


@friend_blueprint.route('/<user_id>', methods=['GET'])
def get_friends(user_id):
    """Get all friends of the user"""
    q1 = [friend.friend_acceptor_id for friend in Friend.query.filter_by(friend_initiator_id=user_id, is_accepted=True)]
    q2 = [friend.friend_initiator_id for friend in Friend.query.filter_by(friend_acceptor_id=user_id, is_accepted=True)]
    return jsonify({
        'status': 'success',
        'friends': q1 + q2,
    })
