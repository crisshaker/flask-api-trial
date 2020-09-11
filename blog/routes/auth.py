from flask import Blueprint, request, jsonify
from blog.database import db
from blog.models import User
import jwt
from blog.config import JWT_SECRET

blueprint = Blueprint('auth', __name__, url_prefix='/auth')


@blueprint.route('/register', methods=['POST'])
def register():
    # TODO: Proper Validation for username and password

    body = request.get_json(force=True)

    username = body.get('username')
    password = body.get('password')

    errors = {}

    if not (username and len(username.strip()) > 0):
        errors['username'] = 'Provide username'

    if not (password and len(password.strip()) > 0):
        errors['password'] = 'Provide password'

    if len(errors):
        return jsonify({'errors': errors}), 400

    username = username.strip().lower()
    username_taken = db.query(User).filter(User.username == username).first()
    if username_taken:
        return jsonify({'errors': {'username': 'username already taken'}})

    user = User(username=username, password=password)
    db.add(user)
    db.commit()
    token = jwt.encode({'user_id': user.id}, JWT_SECRET).decode('utf-8')
    return jsonify({'token': token})


@blueprint.route('/login', methods=['POST'])
def login():
    body = request.json
    username = body['username']
    password = body['password']

    errors = {}

    if not (username and len(username.strip()) > 0):
        errors['username'] = 'Provide username'

    if not (password and len(password.strip()) > 0):
        errors['password'] = 'Provide password'

    if len(errors):
        return jsonify({'errors': errors}), 400

    username = username.lower().strip()
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return jsonify({'error': 'incorrect username or password'}), 401

    if not user.is_correct_password(password):
        return jsonify({'error': 'incorrect username or password'}), 401

    token = jwt.encode({'user_id': user.id}, JWT_SECRET).decode('utf-8')
    return jsonify({'token': token})
