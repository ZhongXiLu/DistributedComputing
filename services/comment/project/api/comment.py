

import json
import requests
from flask import Blueprint, jsonify, request
from sqlalchemy import exc
from requests.exceptions import RequestException, HTTPError
from util.send_request import *
from flask_httpauth import HTTPBasicAuth

from project.api.models import Comment
from project import db

comment_blueprint = Blueprint('comment', __name__, url_prefix='/comments')

auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(user_id_or_token, password):
    response = requests.get('http://authentication:5000/verify_credentials', auth=(user_id_or_token, password))
    if response.status_code == 401:
        return False
    return True


@comment_blueprint.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })


@comment_blueprint.route('', methods=['POST'])
def create_comment():
    """Create a new comment on a post"""
    post_data = request.get_json()
    response_object = {
        'status': 'fail',
        'message': 'Invalid payload.'
    }
    if not post_data:
        return jsonify(response_object), 400

    post_id = post_data.get('post_id')
    user_id = post_data.get('user_id')
    content = post_data.get('content')

    try:
        # Check for bad words
        response_obj = send_request(
            'post', 'anti-cyberbullying', 'anti_cyberbullying/contains_bad_word', timeout=1.5, json={'sentence': str(content)})
        if response_obj.status_code != 201:
            raise RequestException()
        result = response_obj.json
        if result['status'] == "success" and result['result']:    # contains bad word
            response_object['message'] = f'Comment contains bad word: {result["bad_word"]}'
            return jsonify(response_object), 201

        # Update user categories (for ads)
        response_obj = send_request(
            'post', 'ad', f'ads/user/{user_id}', timeout=1.5, json={'sentence': str(content)})
        if response_obj.status_code != 201:
            response_object['message'] = 'failed contacting the ads service'
            raise RequestException()

        db.session.add(Comment(post_id=post_id, creator=user_id, content=content))
        db.session.commit()
        response_object['status'] = 'success'
        response_object['message'] = 'comment was successfully created'
        return jsonify(response_object), 201

    except:
        db.session.rollback()
        return jsonify(response_object), 400


@comment_blueprint.route('/<comment_id>', methods=['GET'])
def get_comment(comment_id):
    """Get a specific comment"""
    response_object = {
        'status': 'fail',
        'message': 'Comment does not exist'
    }
    try:
        comment = Comment.query.filter_by(id=int(comment_id)).first()
        if not comment:
            return jsonify(response_object), 404
        else:
            response_object = {
                'status': 'success',
                'data': {
                    'id': comment.id,
                    'post_id': comment.post_id,
                    'creator': comment.creator,
                    'content': comment.content,
                    'created_date': comment.created_date
                }
            }
            return jsonify(response_object), 200
    except ValueError:
        return jsonify(response_object), 404


@comment_blueprint.route('/<comment_id>', methods=['DELETE'])
def delete_comment(comment_id):
    """Delete a comment on a specific post"""
    response_object = {
        'status': 'fail',
        'message': 'Comment does not exist'
    }
    try:
        comment = Comment.query.filter_by(id=int(comment_id)).first()
        if not comment:
            return jsonify(response_object), 404
        else:
            db.session.delete(comment)
            db.session.commit()
            response_object['status'] = 'success'
            response_object['message'] = 'comment was successfully deleted'
            return jsonify(response_object), 200
    except ValueError:
        return jsonify(response_object), 404


@comment_blueprint.route('/posts/<post_id>', methods=['GET'])
def get_comments_of_post(post_id):
    """Get all the comments on a post"""
    response_object = {
        'status': 'fail',
        'message': 'Comment does not exist'
    }
    try:
        comments = Comment.query.filter_by(post_id=int(post_id))
        response_object = {
            'status': 'success',
            'data': {
                'comments': [comment.to_json() for comment in comments]
            }
        }
        return jsonify(response_object), 200
    except ValueError:
        return jsonify(response_object), 404
