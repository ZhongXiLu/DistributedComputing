from flask import Blueprint, jsonify, request
from sqlalchemy import exc
from util.verify_password import verify_password
from project.api.models import Friend
from project import db

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

    try:
        if Friend.query.filter_by(friend_initiator_id=friend_acceptor_id,
                                  friend_acceptor_id=friend_initiator_id).count():
            response_object['message'] = 'Friendship already exists or is already requested'
            return jsonify(response_object), 400

        db.session.add(Friend(friend_initiator_id=friend_initiator_id, friend_acceptor_id=friend_acceptor_id))
        db.session.commit()
        response_object['status'] = 'success'
        response_object['message'] = 'friendship request was successfully created'
        return jsonify(response_object), 201
    except Exception as e:
        db.session.rollback()
        # response_object["what"] = str(e)
        return jsonify(response_object), 400


@friend_blueprint.route('accept', methods=['put'])
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
        return jsonify(response_object), 200
    except Exception as e:
        db.session.rollback()
        # response_object["what"] = str(e)
        return jsonify(response_object), 400


@friend_blueprint.route('/<friend1_id>/<friend2_id>', methods=['DELETE'])
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


@friend_blueprint.route('/<user_id>', methods=['GET'])
def get_friends(user_id):
    """Get all friends of the user"""
    q1 = Friend.query.filter_by(friend_initiator_id=user_id, is_accepted=True)
    q2 = Friend.query.filter_by(friend_acceptor_id=user_id, is_accepted=True)
    friends = q1.union(q2).all()
    return jsonify({
        'status': 'success',
        'friends': [(x.friend_initiator_id if x.friend_acceptor_id != user_id else x.friend_acceptor_id)
                    for x in friends],
    })