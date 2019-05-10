# services/users/project/api/users.py

import requests
from util.send_request import *
from util.verify_password import verify_password, login_decorator
from requests.exceptions import RequestException, HTTPError
from flask import Blueprint, jsonify, request, g
from sqlalchemy import exc

from project.api.models import User
from project import db

users_blueprint = Blueprint('users', __name__)

import requests
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()


# @auth.verify_password
# def verify_password(user_id_or_token, password):
#     response = requests.get('http://authentication:5000/verify_credentials', auth=(user_id_or_token, password))
#     if response.status_code == 401:
#         return False
#     return True


# class ResponseObj:
#     def __init__(self, response, json, status_code):
#         self.response = response
#         self.json = json
#         self.status_code = status_code
#
#
# def send_request(method: str, service: str, route: str, **kwargs):
#     func = getattr(requests, method.lower())
#     try:
#         response = func(f'http://{service}:5000/{route}', **kwargs)
#         if response:
#             response_object = ResponseObj(response, response.json(), response.status_code)
#         else:
#             response_object = ResponseObj(response, None, response.status_code)
#     except RequestException as e:
#         response_json = {'status': 'fail', 'message': f'{service} service down.', 'error_type': e.__class__.__name__}
#         response_object = ResponseObj(None, response_json, 503)
#     return response_object


@users_blueprint.route('/users/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })


@users_blueprint.route('/users/ping2', methods=['GET'])
def ping2():
    try:
        ret = requests.get('http://authentication:5000/ping', timeout=3)
        ret = ret.json()
    except (ConnectionError, RequestException, TimeoutError):
        ret = {'status': 'fail', 'message': 'authentication service down'}

    except RequestException as e:
        ret = {'status': 'fail', 'message': f'{e}'}
    return jsonify(ret)


@users_blueprint.route('/users/ping3', methods=['GET'])
def ping3():
    response_obj = send_request('get', 'authentication', 'ping', timeout=3)
    return jsonify(response_obj.json), response_obj.status_code


@users_blueprint.route('/users/ping4', methods=['GET'])
@login_decorator
def ping4():
    return jsonify({
        'status': 'success',
        'message': 'pong!',
        'user_id_or_token': g.user_id_or_token,
        'password': g.password,
        'user_id': g.user_id,
    })


@users_blueprint.route('/users', methods=['POST'])
def add_user():
    post_data = request.get_json()
    response_object = {
        'status': 'fail',
        'message': 'Invalid payload.'
    }
    response_code = 400
    if not post_data:
        return jsonify(response_object), 400
    username = post_data.get('username')
    password = post_data.get('password')
    email = post_data.get('email')
    try:
        user = User.query.filter_by(email=email).first()
        if not user:
            user = User(username=username, email=email)
            db.session.add(user)
            db.session.flush()
            db.session.refresh(user)

            response_obj = send_request(
                'post', 'authentication', 'passwords', timeout=3, json={'user_id': user.id, 'password': password})
            response_code = response_obj.status_code
            if response_obj.status_code == 503:
                response_object = response_obj.json
                raise RequestException()
            elif response_obj.status_code != 201:
                raise RequestException()

            db.session.commit()
            response_object['status'] = 'success'
            response_object['message'] = f'{email} was added!'
            response_object['user_id'] = user.id
            return jsonify(response_object), 201
        else:
            response_object['message'] = 'Sorry. That email already exists.'
            return jsonify(response_object), 400
    except (exc.IntegrityError, RequestException) as e:
        db.session.rollback()
        return jsonify(response_object), response_code


@users_blueprint.route('/users/<user_id>', methods=['GET'])
def get_single_user(user_id):
    """Get single user details"""
    response_object = {
        'status': 'fail',
        'message': 'User does not exist'
    }
    try:
        user = User.query.filter_by(id=int(user_id)).first()
        if not user:
            return jsonify(response_object), 404
        else:
            response_object = {
                'status': 'success',
                'data': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'active': user.active
                }
            }
            return jsonify(response_object), 200
    except ValueError:
        return jsonify(response_object), 404


@users_blueprint.route('/users/name/<username>', methods=['GET'])
def get_single_user_by_name(username):
    """Get single user details by username"""
    response_object = {
        'status': 'fail',
        'message': 'User does not exist'
    }
    try:
        user = User.query.filter_by(username=str(username)).first()
        if not user:
            return jsonify(response_object), 404
        else:
            response_object = {
                'status': 'success',
                'data': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'active': user.active
                }
            }
            return jsonify(response_object), 200
    except ValueError:
        return jsonify(response_object), 404


@users_blueprint.route('/users', methods=['GET'])
def get_all_users():
    """Get all users"""
    response_object = {
        'status': 'success',
        'data': {
            'users': [user.to_json() for user in User.query.all()]
        }
    }
    return jsonify(response_object), 200


@users_blueprint.route('/login', methods=['POST'])
def login():
    """Given email & pw, get token"""
    post_data = request.get_json()
    response_object = {
        'status': 'fail',
        'message': 'User does not exist'
    }
    response_code = 400
    if not post_data:
        return jsonify(response_object), 400
    email = post_data.get('email')
    password = post_data.get('password')
    if not email or not password:
        return jsonify(response_object), 400
    try:
        response_code = 404
        user = User.query.filter_by(email=email).first()
        if not user:
            # response_object["sdfqsdf"] = "qsdfqsdf"
            return jsonify(response_object), 404
        else:
            response_obj = send_request(
                'get', 'authentication', 'token', timeout=3, auth=(user.id, password))
            response_code = response_obj.status_code
            if response_obj.status_code == 503:
                response_object = response_obj.json
                raise RequestException()
            elif response_obj.status_code == 401:
                response_object['message'] = "Wrong credentials."
                raise RequestException()
            elif response_obj.status_code != 200:
                raise RequestException()

            response_object = response_obj.json
            response_object["user_id"] = user.id
            return jsonify(response_object), 200
    except (ValueError, RequestException) as e:
        return jsonify(response_object), response_code
