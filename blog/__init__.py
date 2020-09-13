from flask import Flask, jsonify, request
from werkzeug.exceptions import HTTPException
from marshmallow.exceptions import ValidationError
from blog.models import Base, User
from blog.database import engine, db
from blog.routes import auth, posts, users, comments


Base.metadata.create_all(engine)
app = Flask(__name__)
app.url_map.strict_slashes = False


@app.teardown_appcontext
def shutdown_session(exception=None):
    db.remove()


@app.errorhandler(ValidationError)
def marshmallow_validation_error(e):
    print(e)
    return jsonify({'errors': e.messages}), 400


@app.errorhandler(401)
def not_found(e):
    print(e)
    return jsonify({'error': 'UNAUTHORIZED'}), 401


@app.errorhandler(403)
def forbidden(e):
    print(e)
    return jsonify({'error': "You don't have the permission to access the requested resource."}), 403


@app.errorhandler(404)
def not_found(e):
    print(e)
    return jsonify({'error': 'Oops... Not found'}), 404


@app.errorhandler(Exception)
def errorhandler(e):
    print(e)
    return jsonify({'error': 'Request failed'}), 500


app.register_blueprint(auth.blueprint)
app.register_blueprint(posts.blueprint)
app.register_blueprint(users.blueprint)
app.register_blueprint(comments.blueprint)
