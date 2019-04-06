

import requests
import json
import time
from flask import Blueprint, jsonify, request
from flask_httpauth import HTTPBasicAuth

newsfeed_blueprint = Blueprint('newsfeed', __name__, url_prefix='/newsfeed')

auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(user_id_or_token, password):
    response = requests.get('http://authentication:5000/verify_credentials', auth=(user_id_or_token, password))
    if response.status_code == 401:
        return False
    return True


@newsfeed_blueprint.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })


@newsfeed_blueprint.route('/<user_id>', methods=['GET'])
def get_newsfeed(user_id):
    """Get the newsfeed of a user (most recent posts of the followers)"""
    response_object = {
        'status': 'fail',
        'message': 'User does not exist or has not followed anyone yet'
    }
    try:
        posts = []

        # Get the followed users
        headers = {'content-type': 'application/json'}

        # TODO: check url
        response = requests.get(f'http://follow:5000/follows/user/{user_id}', headers=headers)
        data = json.loads(response.data.decode())

        # Get posts of followed users
        for followedUser in data['data']['users']:  # TODO: check 'users'
            response = requests.get(f'http://post:5000/posts/user/{followedUser}', headers=headers)
            data = response.json()
            posts += data['data']['posts']

        # Sort posts (newest first)
        posts.sort(reverse=True, key=lambda x: time.mktime(time.strptime(x['created_date'], '%a, %d %b %Y %H:%M:%S %Z')))

        response_object = {
            'status': 'success',
            'data': {
                'posts': posts
            }
        }
        return jsonify(response_object), 200
    except:
        return jsonify(response_object), 404
