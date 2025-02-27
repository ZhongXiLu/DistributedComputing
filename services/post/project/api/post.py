

import requests, json, time
from collections import Counter
from flask import Blueprint, jsonify, request, g
from sqlalchemy import exc, func
from flask_httpauth import HTTPBasicAuth
from requests.exceptions import RequestException, HTTPError
from util.send_request import *
from util.verify_password import login_decorator

from project.api.models import Post
from project import db

post_blueprint = Blueprint('post', __name__, url_prefix='/posts')

auth = HTTPBasicAuth()


@post_blueprint.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })


@post_blueprint.route('', methods=['POST'])
@login_decorator
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
        # Check for bad words
        response_obj = send_request('post', 'anti-cyberbullying', 'anti_cyberbullying/contains_bad_word',
                                    timeout=3, json={'sentence': str(content)}, auth=(g.user_id_or_token, g.password))
        response_object['anti-cyberbullying'] = response_obj.json
        if response_obj.status_code == 201:
            result = response_obj.json
            if result['status'] == "success" and result['result']:    # contains bad word
                response_object['message'] = f'Post contains bad word: {result["bad_word"]}'
                return jsonify(response_object), 201

        # Update user categories (for ads)
        response_obj = send_request(
            'post', 'ad', f'ads/user/{creator}', timeout=3, json={'sentence': str(content)},
            auth=(g.user_id_or_token, g.password))
        response_object['ad'] = response_obj.json

        # Create post
        post = Post(creator=creator, content=content)
        db.session.add(post)
        db.session.commit()

        if tags:
            # Get user id's by username
            user_tags_ids = []
            for tag in tags:
                response_obj = send_request('get', 'users', f'users/name/{tag}', timeout=3,
                                            auth=(g.user_id_or_token, g.password))
                if response_obj.status_code != 200:
                    continue
                result = response_obj.json
                if result['status'] == "success":
                    user_tags_ids.append(result['data']['id'])

            # Add user tags
            data = {
                'post_id': post.id,
                'user_ids': user_tags_ids
            }
            response_obj = send_request('post', 'tag', 'tags', timeout=3, json=data,
                                        auth=(g.user_id_or_token, g.password))
            response_object['tag'] = response_obj.json

        response_object['status'] = 'success'
        response_object['message'] = 'Post was successfully created'
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


@post_blueprint.route('/stats', methods=['GET'])
def get_post_stats():
    """Get the post statistics"""
    response_object = {
        'status': 'fail',
        'message': 'Post does not exist'
    }
    try:
        posts = ["{}/{}/{}".format(post.created_date.day, post.created_date.month, post.created_date.year) for post in Post.query.all()]
        nr_of_posts_per_day = Counter(posts)

        response_object = {
            'status': 'success',
            'data': {
                'stats': nr_of_posts_per_day
            }
        }
        return jsonify(response_object), 200
    except ValueError:
        return jsonify(response_object), 404


@post_blueprint.route('/<post_id>', methods=['DELETE'])
@login_decorator
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
