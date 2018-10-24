from flask import Blueprint, jsonify, request, render_template
from project.api.models import db, User
from sqlalchemy import exc
users_blueprint = Blueprint('users', __name__, template_folder='./templates')


@users_blueprint.route('/users/ping', methods=['GET'])
def ping_pong():
    return jsonify({'status': "success", 'message': "pong!"})


@users_blueprint.route('/users', methods=['POST'])
def add_user():
    """Create users."""
    user_request_data = request.get_json()

    if not (user_request_data and 'email' in user_request_data and
            'username' in user_request_data):
        return jsonify(
            {'message': 'Invalid payload', 'status': 'fail'}
        ), 400

    if User.query.filter_by(email=user_request_data.get('email')).first():
        return jsonify({
            'message': 'Sorry. That email already exists.',
            'status': 'fail'
        }), 400

    db.session.add(User(
        username=user_request_data.get('username'),
        email=user_request_data.get('email'))
    )
    db.session.commit()
    response_data = {
        'status': "success",
        'message': f"{user_request_data.get('email')} was added"
    }

    return jsonify(response_data), 201


@users_blueprint.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """Get users."""
    try:
        user = User.query.filter_by(uid=user_id).first()
        if not user:
            raise ValueError
    except (ValueError, exc.DataError):
        return jsonify(
            {'status': 'fail', 'message': 'User does not exist'}), 404

    response_object = {
        'status': 'success',
        'data': user.to_json()
    }
    return jsonify(response_object), 200


@users_blueprint.route('/users', methods=['GET'])
def get_users():
    response_object = {
        'status': 'success',
        'data': {
            'users': [user.to_json() for user in User.query.all()]
            }
    }
    return jsonify(response_object), 200


@users_blueprint.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST' and request.form['username'] and \
     request.form['email']:
        db.session.add(User(
            username=request.form['username'],
            email=request.form['email'])
        )
        db.session.commit()
    users = User.query.all()
    return render_template('index.html', users=users)
