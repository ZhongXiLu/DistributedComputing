

import requests
import json
import time
from flask import Blueprint, jsonify, request
from flask_httpauth import HTTPBasicAuth
from requests.exceptions import RequestException, HTTPError
from util.send_request import *

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
        # TODO: check url
        response_obj = send_request('get', 'follow', f'follows/user/{user_id}', timeout=1.5)
        if response_obj.status_code == 503:
            response_object = response_obj.json
            raise RequestException()
        elif response_obj.status_code != 201:
            raise RequestException()

        data = response_obj.json

        # Get posts of followed users
        for followedUser in data['data']['users']:  # TODO: check 'users'
            response_obj = send_request('get', 'post', f'posts/user/{followedUser}', timeout=1.5)
            if response_obj.status_code == 503:
                response_object = response_obj.json
                raise RequestException()
            elif response_obj.status_code != 201:
                raise RequestException()

            data = response_obj.json
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
