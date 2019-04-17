#!/usr/bin/env python
import os
from flask import Flask, abort, request, jsonify, g, url_for
from api.models import User
from api import db
from passlib.apps import custom_app_context as pwd_context
from flask_httpauth import HTTPBasicAuth
from api import app
from api.login import login
import simplejson as json
auth = HTTPBasicAuth()
app.register_blueprint(login)
tokens = ""
@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    user = User.verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = User.query.filter_by(username=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True


@app.route('/api/users/register', methods=['POST'])
def new_user():
    json_received = request.get_json(force=True)
    username = json_received["username"]
    password = json_received["password"]
    admin = json_received["admin"]
    if username is None or password is None:
        abort(400)    # missing arguments
    if User.query.filter_by(username=username).first() is not None:
        abort(400)    # existing user
    user= User(username=username, password_hash=password, admin=admin)
    db.session.add(user)
    db.session.commit()
    return jsonify({'response': 'registration success'})


"""@app.route('/api/users/login', methods=['POST'])
def login_user():
    json_received = request.get_json(force=True)
    username = json_received["username"]
    password = json_received["password"]
    user = User.query.filter_by(username=username).first()
    if pwd_context.verify(password, user.password_hash):
        return jsonify({'response': 'success'})
    else:
        return (password)"""



@app.route('/api/users/<int:id>')
def get_user(id):
    user = User.query.get(id)
    if not user:
        abort(400)
    return jsonify({'username': user.username})


@app.route('/api/users/token', methods=['POST'])
def get_auth_token():
    json_received = request.get_json(force=True)
    username = json_received["username"]
    password = json_received["password"]
    user = User.query.filter_by(username=username).first()
    if password == user.password_hash:
        token = user.generate_auth_token(600)
    return json.dumps({'response': token,'admin': user.admin})


@app.route('/api/users/authentication', methods=['POST'])
def get_resource():
    json_received = request.get_json(force=True)
    username = json_received["username"]
    token = json_received["token"]
    user = User.query.filter_by(username=username).first()
    if user.verify_auth_token(token):
        return json.dumps({'data': 'Hello, %s!' % user.username, 'admin': user.admin})
    else:
        return jsonify({'response': "failed authentication"})


@app.route('/api/users/all', methods=['POST'])
def get_users():
    users = User.query.all()
    userss = []
    
    for user in users:
        jsonObject = {}
        jsonObject['username'] = user.username
        jsonObject['admin'] = user.admin
        userss.append(jsonObject)
    return json.dumps({'users':userss})

@app.route('/api/users/delete', methods=['POST'])
def get_delete():
    json_received = request.get_json(force=True)
    username = json_received["username"]
    user = User.query.filter_by(username=username).first()
    db.session.delete(user)
    db.session.commit()
    return jsonify({'response': "record deleted"})


if __name__ == '__main__':
    if not os.path.exists('db.sqlite'):
        db.create_all()
    app.run(debug=True)