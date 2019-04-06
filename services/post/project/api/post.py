

import requests
import json
from flask import Blueprint, jsonify, request
from sqlalchemy import exc

from project.api.models import Post
from project import db

post_blueprint = Blueprint('post', __name__, url_prefix='/posts')

import requests
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(user_id_or_token, password):
    response = requests.get('http://authentication:5000/verify_credentials', auth=(user_id_or_token, password))
    if response.status_code == 401:
        return False
    return True

@post_blueprint.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })


@post_blueprint.route('', methods=['POST'])
def create_post():
    """Create a new post"""
    post_data = request.get_json()
    response_object = {
        'status': 'fail',
        'message': 'Invalid payload.'
    }
    if not post_data:
        return jsonify(response_object), 400

    creator = post_data.get('creator')
    content = post_data.get('content')
    tags = post_data.get('tags')

    try:
        post = Post(creator=creator, content=content)
        db.session.add(post)
        db.session.commit()
        if tags:
            headers = {'content-type': 'application/json'}
            data = {
                'post_id': post.id,
                'user_ids': tags
            }
            response = requests.post('http://tag:5000/tags', data=json.dumps(data), headers=headers)
            if response.status_code != 201:
                raise Exception("Failed adding tags to post")

        response_object['status'] = 'success'
        response_object['message'] = 'post was successfully created'
        return jsonify(response_object), 201

    except:
        db.session.rollback()
        return jsonify(response_object), 400


@post_blueprint.route('/<post_id>', methods=['GET'])
def get_post(post_id):
    """Get a specific post"""
    response_object = {
        'status': 'fail',
        'message': 'Post does not exist'
    }
    try:
        post = Post.query.filter_by(id=int(post_id)).first()
        if not post:
            return jsonify(response_object), 404
        else:
            response_object = {
                'status': 'success',
                'data': {
                    'id': post.id,
                    'creator': post.creator,
                    'content': post.content,
                    'created_date': post.created_date
                }
            }
            return jsonify(response_object), 200
    except ValueError:
        return jsonify(response_object), 404


@post_blueprint.route('/<post_id>', methods=['DELETE'])
def delete_post(post_id):
    """Delete a specific post"""
    response_object = {
        'status': 'fail',
        'message': 'Post does not exist'
    }
    try:
        post = Post.query.filter_by(id=int(post_id)).first()
        if not post:
            return jsonify(response_object), 404
        else:
            db.session.delete(post)
            db.session.commit()
            response_object['status'] = 'success'
            response_object['message'] = 'post was successfully deleted'
            return jsonify(response_object), 200
    except ValueError:
        return jsonify(response_object), 404


@post_blueprint.route('/user/<user_id>', methods=['GET'])
def get_post_of_user(user_id):
    """Get all the posts from a user"""
    response_object = {
        'status': 'fail',
        'message': 'Post does not exist'
    }
    try:
        posts = Post.query.filter_by(creator=int(user_id))
        response_object = {
            'status': 'success',
            'data': {
                'posts': [post.to_json() for post in posts]
            }
        }
        return jsonify(response_object), 200
    except ValueError:
        return jsonify(response_object), 404
