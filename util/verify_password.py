import requests
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(user_id_or_token, password):
    response = requests.get('http://authentication:5000/verify_credentials', auth=(user_id_or_token, password))
    if response.status_code == 401:
        return False
    return True
