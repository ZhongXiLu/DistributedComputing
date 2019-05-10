# services/users/project/api/users.py
import requests

from flask import Blueprint, jsonify, request, g
from sqlalchemy import exc

from project.api.models import Password
from project import db
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()

authentication_blueprint = Blueprint('authentication', __name__)

"""
Tutorial: https://blog.miguelgrinberg.com/post/restful-authentication-with-flask

Add password:
[POST]: /passwords
user_id  # type: int
password  # type: string
is_admin  # type: bool (optional)
Returns: user_id

Update password 
[PUT]: /passwords
(login_required)
password  # type: string
Returns: user_id

Delete password 
[DELETE]: /passwords
(login_required)
Returns: user_id


Verify user_id + password
[POST]: /verify_credentials
user_id  # type: int
password  # type: string
Returns: user_id + (True | False)

Get token
[GET]: /token
(login_required)
Returns: user_id

Authenticate

"""


@authentication_blueprint.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })


@authentication_blueprint.route('/ping_auth', methods=['GET'])
@auth.login_required
def ping_pong_login_required():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })


@authentication_blueprint.route('/passwords', methods=['POST'])
def add_password():
    post_data = request.get_json()
    response_object = {
        'status': 'fail',
        'message': 'Invalid payload.'
    }
    if not post_data:
        return jsonify(response_object), 400
    user_id = post_data.get('user_id')
    password = post_data.get('password')
    is_admin = post_data.get('is_admin')

    try:
        user_id = int(str(user_id))
    except (ValueError, TypeError):
        return jsonify(response_object), 400
    if password is None:
        return jsonify(response_object), 400

    if is_admin is None:
        is_admin = False

    try:
        pw = Password.query.filter_by(user_id=user_id).first()
        if not pw:
            db.session.add(Password(user_id=user_id, password=str(password), is_admin=is_admin))
            db.session.commit()
            response_object['status'] = 'success'
            response_object['message'] = f'{user_id}\'s password was added!'
            return jsonify(response_object), 201
        else:
            response_object['message'] = f'User {user_id} already exists.'
            return jsonify(response_object), 400
    except exc.IntegrityError:
        db.session.rollback()
        return jsonify(response_object), 400


@authentication_blueprint.route('/passwords', methods=['PUT'])
@auth.login_required
def update_password():
    put_data = request.get_json()
    response_object = {
        'status': 'fail',
        'message': 'Invalid payload.'
    }
    if not put_data:
        response_object['error'] = 'No data received.'
        return jsonify(response_object), 400
    password = put_data.get('password')
    if password is None:
        response_object['error'] = 'Password is None.'
        return jsonify(response_object), 400
    try:
        pw = Password.query.filter_by(user_id=auth.username()).first()  # type: Password
        if pw:
            pw.set_password(password)
            db.session.commit()
            response_object['status'] = 'success'
            response_object['message'] = f'Changed password of user {auth.username()}'
            return jsonify(response_object), 200
    except exc.IntegrityError:
        db.session.rollback()
    return jsonify(response_object), 400


@authentication_blueprint.route('/passwords', methods=['DELETE'])
@auth.login_required
def delete_password():
    response_object = {
        'status': 'fail',
        'message': 'Invalid payload.'
    }
    try:
        pw = Password.query.filter_by(user_id=auth.username()).first()  # type: Password
        if pw:
            db.session.delete(pw)
            db.session.commit()
            response_object['status'] = 'success'
            response_object['message'] = f'Deleted password of user {auth.username()}'
            return jsonify(response_object), 200
    except exc.IntegrityError:
        db.session.rollback()
    return jsonify(response_object), 400


@authentication_blueprint.route('/verify_credentials', methods=['GET'])
@auth.login_required
def verify_credentials():
    return jsonify({
        'status': 'success',
        'authorized': True,
        'user_id': g.user_id
    }), 200


@authentication_blueprint.route('/token', methods=['GET'])
@auth.login_required
def get_auth_token():
    pw = g.pw  # type: Password
    token = pw.generate_auth_token()
    return jsonify({
        'status': 'success',
        'token': token.decode('ascii')
    }), 200


@authentication_blueprint.route('/is_admin', methods=['PUT'])
def is_admin():
    put_data = request.get_json()
    response_object = {
        'status': 'fail',
        'message': 'Invalid payload.'
    }
    if not put_data:
        return jsonify(response_object), 400
    user_id = put_data.get('user_id')
    try:
        user_id = int(str(user_id))
    except (ValueError, TypeError):
        return jsonify(response_object), 400

    pw = Password.query.filter_by(user_id=user_id).first()  # type: Password
    response_object['status'] = 'success'
    response_object['message'] = 'successfully got is_admin'
    response_object['is_admin'] = pw.is_admin
    return jsonify(response_object), 200


@auth.verify_password
def verify_password(user_id_or_token, password):
    # Try to authenticate with token
    g.user_id = None
    pw = Password.verify_auth_token(user_id_or_token)
    if not pw:
        # Try to authenticate with user_id + pw
        try:
            pw = Password.query.filter_by(user_id=int(user_id_or_token)).first()
        except ValueError:
            pass
        if not pw or not pw.verify_password(password):
            return False
    g.pw = pw
    g.user_id = pw.user_id
    return True




