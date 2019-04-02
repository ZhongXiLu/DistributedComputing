# services/users/project/api/users.py
import numbers

from flask import Blueprint, jsonify, request
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



@authentication_blueprint.route('/authentication/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })


@authentication_blueprint.route('/authentication', methods=['POST'])
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

    try:
        user_id = int(str(user_id))
    except (ValueError, TypeError):
        return jsonify(response_object), 400
    if password is None:
        return jsonify(response_object), 400

    try:
        pw = Password.query.filter_by(user_id=user_id).first()
        if not pw:
            db.session.add(Password(user_id=user_id, password=str(password)))
            db.session.commit()
            response_object['status'] = 'success'
            response_object['message'] = f'{user_id}\'s password was added!'

            # pw1 = Password.query.filter_by(user_id=user_id).first()
            # print(pw1.to_json())

            return jsonify(response_object), 201
        else:
            response_object['message'] = f'User {user_id} already exists.'
            return jsonify(response_object), 400
    except exc.IntegrityError:
        db.session.rollback()
        return jsonify(response_object), 400


@authentication_blueprint.route('/authentication/ping2', methods=['GET'])
@auth.login_required
def ping_pong_login_required():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })

@auth.verify_password
def verify_password(user_id, password):
    # pw = Password.verify_auth_token(user_id)
    pw = Password.query.filter_by(user_id=int(user_id)).first()
    if not pw or not pw.verify_password(password):
        return False
    return True


@authentication_blueprint.route('/authentication/verify_password')
def verify_password_rest(user_id, password):
    pass


'''@authentication_blueprint.route('/users/<user_id>', methods=['GET'])
def get_single_user(user_id):
    """Get single user details"""
    response_object = {
        'status': 'fail',
        'message': 'User does not exist'
    }
    try:
        user = Password.query.filter_by(id=int(user_id)).first()
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
        return jsonify(response_object), 404'''

