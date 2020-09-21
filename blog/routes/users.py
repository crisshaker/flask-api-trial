from flask import Blueprint, jsonify
from blog.database import db
from blog.models import User
from blog.schemas import UserSchema

blueprint = Blueprint('users', __name__, url_prefix='/users')


@blueprint.route('/', methods=['GET'])
def get_all_users():
    users = db.query(User).all()
    users[98]

    return jsonify(UserSchema().dump(users, many=True))
