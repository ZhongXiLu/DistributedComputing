

import json
import requests
from flask import Blueprint, jsonify, request
from sqlalchemy import exc
from requests.exceptions import RequestException, HTTPError
from util.send_request import *
from util.verify_password import login_decorator
from flask_httpauth import HTTPBasicAuth

from project.api.models import Notification
from project import db

notification_blueprint = Blueprint('notification', __name__, url_prefix='/notifications')

auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(user_id_or_token, password):
    response = requests.get('http://authentication:5000/verify_credentials', auth=(user_id_or_token, password))
    if response.status_code == 401:
        return False
    return True


@notification_blueprint.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })


@notification_blueprint.route('', methods=['POST'])
@login_decorator
def create_notification():
    """Create a new notification for users"""
    post_data = request.get_json()
    response_object = {
        'status': 'fail',
        'message': 'Invalid payload.'
    }
    if not post_data:
        return jsonify(response_object), 400

    content = post_data.get('content')
    recipients = post_data.get('recipients')

    try:
        for recipient in recipients:
            db.session.add(Notification(content=content, recipient=recipient))
        db.session.commit()
        response_object['status'] = 'success'
        response_object['message'] = 'Notifications were successfully created'
        return jsonify(response_object), 201

    except:
        db.session.rollback()
        return jsonify(response_object), 400


@notification_blueprint.route('/<notification_id>', methods=['GET'])
def get_notification(notification_id):
    """Get a specific notification"""
    response_object = {
        'status': 'fail',
        'message': 'Notification does not exist'
    }
    try:
        notification = Notification.query.filter_by(id=int(notification_id)).first()
        if not notification:
            return jsonify(response_object), 404
        else:
            response_object = {
                'status': 'success',
                'data': {
                    'id': notification.id,
                    'content': notification.content,
                    'recipient': notification.recipient,
                    'is_read': notification.is_read,
                    'created_date': notification.created_date
                }
            }
            return jsonify(response_object), 200
    except ValueError:
        return jsonify(response_object), 404


@notification_blueprint.route('/<notification_id>', methods=['PUT'])
@login_decorator
def mark_notification_as_read(notification_id):
    """Mark a notification as read"""
    response_object = {
        'status': 'fail',
        'message': 'Notification does not exist'
    }
    try:
        notification = Notification.query.filter_by(id=int(notification_id)).first()
        if not notification:
            return jsonify(response_object), 404
        else:
            notification.is_read = True
            db.session.commit()
            response_object['status'] = 'success'
            response_object['message'] = 'Notification was successfully marked as read'
            return jsonify(response_object), 200
    except ValueError:
        return jsonify(response_object), 404


@notification_blueprint.route('/user/<user_id>', methods=['GET'])
@login_decorator
def get_notifications_user(user_id):
    """Get all the unread notifications of a user"""
    response_object = {
        'status': 'fail',
        'message': 'User does not exist'
    }
    try:
        notifications = Notification.query.filter_by(recipient=int(user_id), is_read=False)
        response_object = {
            'status': 'success',
            'data': {
                'notifications': [notification.to_json() for notification in notifications]
            }
        }
        return jsonify(response_object), 200
    except ValueError:
        return jsonify(response_object), 404
