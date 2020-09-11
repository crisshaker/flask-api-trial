from functools import wraps
from flask import request, abort, g
import jwt
from blog.config import JWT_SECRET
from blog.database import db
from blog.models import User


def require_login(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            abort(401)
        try:
            payload = jwt.decode(token, JWT_SECRET)
        except jwt.exceptions.InvalidSignatureError:
            abort(401)
        user = db.query(User.id, User.username).filter(
            User.id == payload['user_id']).first()
        if not user:
            abort(401)
        g.user = user

        return func(*args, **kwargs)

    return wrapped
