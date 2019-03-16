

from flask import Blueprint, jsonify, request
from sqlalchemy import exc

from project.api.models import Post
from project import db

post_blueprint = Blueprint('post', __name__, url_prefix='/posts')


@post_blueprint.route('', methods=['POST'])
def create_post():
    """Create a new post"""
    post_data = request.get_json()
    response_object = {
        'status': 'fail',
        'message': 'Invalid payload.'
    }
    if not post_data:
        return jsonify(response_object), 400

    creator = post_data.get('creator')
    content = post_data.get('content')
    tags = post_data.get('tags')

    try:
        db.session.add(Post(creator=creator, content=content))
        db.session.commit()
        # TODO: Add tags to post by calling the Tag service
        response_object['status'] = 'success'
        return jsonify(response_object), 201

    except exc.IntegrityError:
        db.session.rollback()
        return jsonify(response_object), 400


@post_blueprint.route('/<post_id>', methods=['GET'])
def get_post(post_id):
    """Get a specific post"""
    response_object = {
        'status': 'fail',
        'message': 'Post does not exist'
    }
    try:
        post = Post.query.filter_by(id=int(post_id)).first()
        if not post:
            return jsonify(response_object), 404
        else:
            response_object = {
                'status': 'success',
                'data': {
                    'id': post.id,
                    'creator': post.creator,
                    'content': post.content,
                    'created_date': post.created_date
                }
            }
            return jsonify(response_object), 200
    except ValueError:
        return jsonify(response_object), 404


@post_blueprint.route('/user/<user_id>', methods=['GET'])
def get_post_of_user(user_id):
    """Get all the posts from a user"""
    response_object = {
        'status': 'fail',
        'message': 'User did not post anything yet'
    }
    try:
        posts = Post.query.filter_by(creator=int(user_id))
        if not posts:
            return jsonify(response_object), 404
        else:
            response_object = {
                'status': 'success',
                'data': {
                    'posts': [post.to_json() for post in posts]
                }
            }
            return jsonify(response_object), 200
    except ValueError:
        return jsonify(response_object), 404
