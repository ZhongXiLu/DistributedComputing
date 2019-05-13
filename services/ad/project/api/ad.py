

import os, requests, json, re
from flask import Blueprint, jsonify, request, render_template, send_from_directory, g
from flask_httpauth import HTTPBasicAuth
from sqlalchemy import exc
from util.verify_password import login_decorator, is_admin

from project.api.models import Ad, UserCategory
from project import db

ad_blueprint = Blueprint('ad', __name__, url_prefix='/ads')


auth = HTTPBasicAuth()


@ad_blueprint.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })


@ad_blueprint.route('', methods=['GET'])
@login_decorator
def index():
    response_object = {
        'status': 'fail',
        'message': 'Unauthorized access: user is not an admin'
    }

    try:
        admin = is_admin(g.user_id)
        if admin:
            images = [ad.to_json() for ad in Ad.query.all()]
            return render_template("index.html", images=images)
        else:
            return jsonify(response_object), 401
    except:
        return jsonify(response_object), 401


@ad_blueprint.route('/<filename>', methods=['GET'])
def send_file(filename):
    return send_from_directory(os.path.abspath(os.path.basename('uploads')), filename)


@ad_blueprint.route('', methods=['POST'])
@login_decorator
def create_ad():
    """Add a new ad"""
    response_object = {
        'status': 'fail',
        'message': 'Invalid payload.'
    }

    # Save image to local filesystem
    file = request.files['image']
    uploadDir = os.path.abspath(os.path.basename('uploads'))
    if not os.path.exists(uploadDir):
        os.makedirs(uploadDir)
    filename = os.path.join(uploadDir, file.filename)
    file.save(filename)

    categories = str(request.form.get('category')).lower().split(' ')
    for category in categories:
        newCategory = re.sub(r'[\W_]+', '', str(category).lower())
        db.session.add(Ad(category=newCategory, image=file.filename))

    db.session.commit()
    response_object['status'] = 'success'
    response_object['message'] = 'Ad was successfully added'
    return jsonify(response_object), 201


@ad_blueprint.route('/user/<user_id>', methods=['POST'])
@login_decorator
def update_category(user_id):
    """Update (if necessary) the categories of a user (personalized ads)"""
    post_data = request.get_json()
    response_object = {
        'status': 'fail',
    }
    if not post_data:
        return jsonify(response_object), 400

    sentence = post_data.get('sentence')

    try:
        response_object['result'] = False

        categories = [ad.category for ad in Ad.query.distinct(Ad.category)]
        words = sentence.lower().split(' ')
        for word in words:
            if re.sub(r'[\W_]+', '', str(word).lower()) in categories:
                # sentence contains category word
                if UserCategory.query.filter_by(user_id=user_id, category=word).count() == 0:
                    db.session.add(UserCategory(user_id=user_id, category=word))

        db.session.commit()
        response_object['status'] = 'success'
        return jsonify(response_object), 201

    except:
        db.session.rollback()
        return jsonify(response_object), 400


@ad_blueprint.route('/user/<user_id>', methods=['GET'])
@login_decorator
def get_personalized_ads(user_id):
    """Get ads specifically targeted to a user if any"""
    response_object = {
        'status': 'fail',
        'message': 'User has no personalized ads'
    }
    try:
        categories = UserCategory.query.filter_by(user_id=user_id)
        ads = []
        if categories:
            # User has user-specific ads
            for category in categories:
                ads += Ad.query.filter_by(category=category.category)
        else:
            # User has no categories yet, so return all
            ads = Ad.query.all()

        response_object = {
            'status': 'success',
            'data': {
                'ads': [ad.to_json() for ad in ads]
            }
        }
        return jsonify(response_object), 200
    except ValueError:
        return jsonify(response_object), 404



