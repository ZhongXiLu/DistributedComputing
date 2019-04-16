

import requests
import json
import re
from flask import Blueprint, jsonify, request, render_template
from flask_httpauth import HTTPBasicAuth
from sqlalchemy import exc

from project.api.models import BadWord
from project import db

anti_cyberbullying_blueprint = Blueprint('anti-cyberbullying', __name__, url_prefix='/anti_cyberbullying')


auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(user_id_or_token, password):
    response = requests.get('http://authentication:5000/verify_credentials', auth=(user_id_or_token, password))
    if response.status_code == 401:
        return False
    return True


@anti_cyberbullying_blueprint.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })


@anti_cyberbullying_blueprint.route('', methods=['GET'])
def index():
    words = [word.to_json() for word in BadWord.query.all()]
    return render_template("index.html", words=words)


@anti_cyberbullying_blueprint.route('', methods=['POST'])
def create_bad_word():
    """Add a new bad word"""
    response_object = {
        'status': 'fail',
        'message': 'Invalid payload.'
    }

    try:
        words = str(request.form.get('word')).lower().split(' ')
        for word in words:
            if BadWord.query.filter_by(word=word).count() == 0:
                db.session.add(BadWord(word=re.sub(r'[\W_]+', '', word)))

        db.session.commit()
        response_object['status'] = 'success'
        response_object['message'] = 'Bad words were successfully added'
        return jsonify(response_object), 201

    except:
        db.session.rollback()
        return jsonify(response_object), 400


@anti_cyberbullying_blueprint.route('/contains_bad_word', methods=['POST'])
def contains_bad_word():
    """Check if a sentence contains a bad word from the database"""
    post_data = request.get_json()
    response_object = {
        'status': 'fail',
    }
    if not post_data:
        return jsonify(response_object), 400

    sentence = post_data.get('sentence')

    try:
        response_object['result'] = False

        words = sentence.lower().split(' ')

        for word in words:
            if BadWord.query.filter_by(word=word).count() > 0:
                # found bad words in sentence
                response_object['result'] = True
                response_object['bad_word'] = word

        response_object['status'] = 'success'
        return jsonify(response_object), 201

    except:
        db.session.rollback()
        return jsonify(response_object), 400


# TODO: request to remove bad word from database?

@anti_cyberbullying_blueprint.route('/bad_words', methods=['GET'])
def get_bad_words():
    """Get all the bad words"""
    response_object = {
        'status': 'success',
        'data': {
            'words': [word.to_json() for word in BadWord.query.all()]
        }
    }
    return jsonify(response_object), 200
