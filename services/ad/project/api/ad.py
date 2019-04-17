

import os
import requests
import json
import re
from flask import Blueprint, jsonify, request, render_template, send_from_directory
from flask_httpauth import HTTPBasicAuth
from sqlalchemy import exc

from project.api.models import Ad
from project import db

ad_blueprint = Blueprint('ad', __name__, url_prefix='/ads')


auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(user_id_or_token, password):
    response = requests.get('http://authentication:5000/verify_credentials', auth=(user_id_or_token, password))
    if response.status_code == 401:
        return False
    return True


@ad_blueprint.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })


@ad_blueprint.route('', methods=['GET'])
def index():
    images = [ad.to_json() for ad in Ad.query.all()]
    return render_template("index.html", images=images)


@ad_blueprint.route('/<filename>', methods=['GET'])
def send_file(filename):
    return send_from_directory(os.path.abspath(os.path.basename('uploads')), filename)


@ad_blueprint.route('', methods=['POST'])
def create_ad():
    """Add a new ad"""
    response_object = {
        'status': 'fail',
        'message': 'Invalid payload.'
    }

    category = re.sub(r'[\W_]+', '', str(request.form.get('category')).lower())

    # Save image to local filesystem
    file = request.files['image']
    uploadDir = os.path.abspath(os.path.basename('uploads'))
    if not os.path.exists(uploadDir):
        os.makedirs(uploadDir)
    filename = os.path.join(uploadDir, file.filename)
    file.save(filename)
    db.session.add(Ad(category=category, image=file.filename))

    db.session.commit()
    response_object['status'] = 'success'
    response_object['message'] = 'Ad was successfully added'
    return jsonify(response_object), 201


@ad_blueprint.route('/user/<user_id>', methods=['GET'])
def get_personalized_ads(user_id):
    """Get ads specifically targeted to a user if any"""
    # TODO

    # Now just return every ad
    response_object = {
        'status': 'fail',
        'message': 'User has no personalized ads'
    }
    try:
        ads = Ad.query.all()
        response_object = {
            'status': 'success',
            'data': {
                'posts': [ad.to_json() for ad in ads]
            }
        }
        return jsonify(response_object), 200
    except ValueError:
        return jsonify(response_object), 404



