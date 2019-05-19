import os
import requests
from flask import g
from flask_httpauth import HTTPBasicAuth
from util.send_request import send_request

auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(user_id_or_token_or_username, password):
    if os.environ.get('TESTING') == "True":
        g.user_id_or_token = ""
        g.password = ""
        return True

    response_obj = send_request('get', 'users', f'users/name/{user_id_or_token_or_username}', timeout=3)
    if response_obj.status_code == 200:
        user_id_or_token_or_username = response_obj.json['data']['id']

    response = send_request(
        'get', 'authentication', 'verify_credentials', timeout=3, auth=(user_id_or_token_or_username, password))
    if response.status_code == 401:
        g.reason = 'Wrong credentials'
        return False
    elif response.status_code != 200:
        g.reason = 'Other reason'
        return False
    try:
        g.user_id = response.json['user_id']
    except KeyError:
        g.user_id = None
    g.user_id_or_token = user_id_or_token_or_username
    g.password = password
    return True


def is_admin(user_id):
    response = send_request('put', 'authentication', 'is_admin', timeout=3, json={'user_id': user_id})
    return response.json['is_admin']

login_decorator = auth.login_required