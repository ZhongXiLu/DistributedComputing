

from flask import Blueprint, jsonify, request
from sqlalchemy import exc
from util.send_request import *
from util.verify_password import login_decorator

from project.api.models import Like
from project import db

import requests
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()

like_blueprint = Blueprint('like', __name__, url_prefix='/likes')


@like_blueprint.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })


@like_blueprint.route('', methods=['POST'])
@login_decorator
def create_like():
    """Create a new like on a post"""
    post_data = request.get_json()
    response_object = {
        'status': 'fail',
        'message': 'Invalid payload.'
    }
    if not post_data:
        return jsonify(response_object), 400

    post_id = post_data.get('post_id')
    user_id = post_data.get('user_id')

    try:
        # Send notification to creator of post
        try:
            response_obj = send_request('get', 'post', f'posts/{post_id}', timeout=3, auth=(auth.username(), None))
            creator = response_obj.json['data']['creator']

            response_obj = send_request('get', 'users', f'users/{user_id}', timeout=3, auth=(auth.username(), None))
            username = response_obj.json['data']['username']

            send_request('post', 'notification', 'notifications', timeout=3,
                         json={'content': f'{username} has liked your post', 'recipients': [creator]},
                         auth=(auth.username(), None))
        except:
            response_object['warning'] = 'failed creating a notification'

        db.session.add(Like(post_id=post_id, user_id=user_id))
        db.session.commit()
        response_object['status'] = 'success'
        response_object['message'] = 'like was successfully created'
        return jsonify(response_object), 201

    except:
        db.session.rollback()
        return jsonify(response_object), 400


@like_blueprint.route('/posts/<post_id>', methods=['DELETE'])
@login_decorator
def delete_like(post_id):
    """Undo a like on a specific post"""
    post_data = request.get_json()
    response_object = {
        'status': 'fail',
        'message': 'Like does not exist'
    }

    user_id = post_data.get('user_id')

    try:
        like = Like.query.filter(Like.user_id == int(user_id), Like.post_id == int(post_id)).first()

        if not like:
            return jsonify(response_object), 404
        else:
            db.session.delete(like)
            db.session.commit()
            response_object['status'] = 'success'
            response_object['message'] = 'like was successfully removed'
            return jsonify(response_object), 200

    except ValueError:
        return jsonify(response_object), 404


@like_blueprint.route('/posts/<post_id>', methods=['GET'])
def get_likes_of_post(post_id):
    """Get all the likes on a post"""
    response_object = {
        'status': 'fail',
        'message': 'Like does not exist'
    }
    try:
        likes = Like.query.filter_by(post_id=int(post_id))
        response_object = {
            'status': 'success',
            'data': {
                'likes': [like.to_json() for like in likes]
            }
        }
        return jsonify(response_object), 200
    except ValueError:
        return jsonify(response_object), 404
