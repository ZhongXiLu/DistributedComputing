

from flask import Blueprint, jsonify, request, g
from sqlalchemy import exc
from util.verify_password import verify_password
from project.api.models import Follower
from project import db
from util.send_request import *
from util.verify_password import login_decorator

import requests
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()

follow_blueprint = Blueprint('follow', __name__, url_prefix='/follow')


@follow_blueprint.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })


@follow_blueprint.route('', methods=['POST'])
@login_decorator
def create_follow():
    """Create follower-followee relation"""
    post_data = request.get_json()
    response_object = {
        'status': 'fail',
        'message': 'Invalid payload.'
    }
    if not post_data:
        return jsonify(response_object), 400

    follower_id = post_data.get('follower_id')
    followee_id = post_data.get('followee_id')
    if follower_id is None or followee_id is None:
        return jsonify(response_object), 400

    try:
        # Send notification to followee
        try:
            response_obj = send_request('get', 'users', f'users/{follower_id}', timeout=3, auth=(auth.username(), None))
            response_object['users'] = response_obj.json
            username = response_obj.json['data']['username']

            send_request('post', 'notification', 'notifications', timeout=3,
                         json={'content': f'{username} has followed you', 'recipients': [followee_id]},
                         auth=(auth.username(), None))
            response_object['notification'] = response_obj.json
        except:
            response_object['warning'] = 'failed creating a notification'

        db.session.add(Follower(follower_id=follower_id, followee_id=followee_id))
        db.session.commit()
        response_object['status'] = 'success'
        response_object['message'] = 'follower was successfully created'

        # Get name of follower
        r_obj = send_request('get', 'users', f'users/{follower_id}', timeout=3,
                             auth=(g.user_id_or_token, g.password))
        try:
            follower_name = r_obj.json['data']['username']
        except KeyError:
            follower_name = f'User {follower_id}'

        # Send notification to acceptor
        r_obj = send_request('post', 'notification', 'notifications', timeout=3,
                             json={'content': f'{follower_name} has started following you',
                                   'recipients': [followee_id]},
                             auth=(g.user_id_or_token, g.password))
        response_object['notification'] = r_obj.json

        return jsonify(response_object), 201
    except Exception as e:
        db.session.rollback()
        # response_object["what"] = str(e)
        return jsonify(response_object), 400


@follow_blueprint.route('/<follower_id>/<followee_id>', methods=['DELETE'])
@login_decorator
def delete_follow(follower_id, followee_id):
    """Delete a follower followee relation"""
    response_object = {
        'status': 'fail',
        # 'message': 'Invalid payload.'
    }
    try:
        follower = Follower.query.filter_by(follower_id=follower_id, followee_id=followee_id).first()
        if follower:
            db.session.delete(follower)
            db.session.commit()
            response_object['status'] = 'success'
            response_object['message'] = f'{follower_id} stopped following {followee_id}'
            return jsonify(response_object), 200
    except exc.IntegrityError:
        db.session.rollback()
    return jsonify(response_object), 400


@follow_blueprint.route('/followees/<follower_id>', methods=['GET'])
def get_followees(follower_id):
    """Get all users the follower follows"""
    followees = Follower.query.filter_by(follower_id=follower_id).all()
    return jsonify({'status': 'success', 'followees': [x.followee_id for x in followees]}), 200


@follow_blueprint.route('/followers/<followee_id>', methods=['GET'])
def get_followers(followee_id):
    """Get all followers of the user"""
    followers = Follower.query.filter_by(followee_id=followee_id).all()
    return jsonify({'status': 'success', 'followers': [x.follower_id for x in followers]}), 200
