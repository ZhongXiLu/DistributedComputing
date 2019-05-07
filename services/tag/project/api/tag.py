

from flask import Blueprint, jsonify, request
from sqlalchemy import exc
from util.send_request import *
from util.verify_password import login_decorator

from project.api.models import Tag
from project import db

tag_blueprint = Blueprint('tag', __name__, url_prefix='/tags')

import requests
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()


@tag_blueprint.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })


@tag_blueprint.route('', methods=['POST'])
@login_decorator
def create_tags():
    """Create new tags on a post"""
    post_data = request.get_json()
    response_object = {
        'status': 'fail',
        'message': 'Invalid payload.'
    }
    if not post_data:
        return jsonify(response_object), 400

    post_id = post_data.get('post_id')
    user_ids = post_data.get('user_ids')

    try:
        # Send notification to the tagged person
        try:
            response_obj = send_request('get', 'post', f'posts/{post_id}', timeout=3)
            creator = response_obj.json['data']['creator']

            response_obj = send_request('get', 'users', f'users/{creator}', timeout=3)
            username = response_obj.json['data']['username']

            send_request('post', 'notification', 'notifications', timeout=3,
                         json={'content': f'{username} has tagged you in their post', 'recipients': user_ids})
        except:
            response_object['warning'] = 'failed creating a notification'

        for user_id in user_ids:
            db.session.add(Tag(post_id=post_id, user_id=user_id))
        db.session.commit()
        response_object['status'] = 'success'
        response_object['message'] = 'tags were successfully created'
        return jsonify(response_object), 201

    except:
        db.session.rollback()
        return jsonify(response_object), 400


@tag_blueprint.route('/posts/<post_id>', methods=['GET'])
def get_tags_of_post(post_id):
    """Get all the tags on a post"""
    response_object = {
        'status': 'fail',
        'message': 'Tag does not exist'
    }
    try:
        tags = Tag.query.filter_by(post_id=int(post_id))
        response_object = {
            'status': 'success',
            'data': {
                'tags': [tag.to_json() for tag in tags]
            }
        }
        return jsonify(response_object), 200
    except ValueError:
        return jsonify(response_object), 404
