import requests
from flask_httpauth import HTTPBasicAuth
from util.send_request import send_request

auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(user_id_or_token, password):
    response = send_request(
        'get', 'authentication', 'verify_credentials', timeout=3, auth=(user_id_or_token, password))
    if response.status_code == 401:
        return False
    return True


def is_admin(user_id):
    response = send_request('put', 'authentication', 'is_admin', timeout=3, json={'user_id': user_id})
    return response.json['is_admin']
