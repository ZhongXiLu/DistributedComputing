from flask import Blueprint, request, jsonify
from passlib.apps import custom_app_context as pwd_context
from api.models import User
login = Blueprint('login', __name__)
@login.route('/api/users/login', methods=['POST'])
def login_user():
    json_received = request.get_json(force=True)
    username = json_received["username"]
    password = json_received["password"]
    user = User.query.filter_by(username=username).first()
    if pwd_context.verify(password, user.password_hash):
        return jsonify({'response': 'success'})
    else:
        return (password)