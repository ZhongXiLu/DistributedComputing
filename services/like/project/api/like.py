

from flask import Blueprint, jsonify, request
from sqlalchemy import exc

from project.api.models import Like
from project import db

import requests
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth

like_blueprint = Blueprint('like', __name__, url_prefix='/likes')

@auth.verify_password
def verify_password(user_id_or_token, password):
    response = requests.get('http://authentication:5000/verify_credentials', auth=(user_id_or_token, password))
    if response.status_code == 401:
        return False
    return True


@like_blueprint.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })


@like_blueprint.route('', methods=['POST'])
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
        db.session.add(Like(post_id=post_id, user_id=user_id))
        db.session.commit()
        response_object['status'] = 'success'
        response_object['message'] = 'like was successfully created'
        return jsonify(response_object), 201

    except:
        db.session.rollback()
        return jsonify(response_object), 400


@like_blueprint.route('/posts/<post_id>', methods=['DELETE'])
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
