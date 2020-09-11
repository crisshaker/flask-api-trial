from flask import Blueprint, jsonify, request, abort, g
from blog.database import db
from blog.models import Post
from blog.schemas import PostSchema
from blog.decorators import require_login

blueprint = Blueprint('posts', __name__, url_prefix='/posts')


@blueprint.route('/', methods=['GET'])
@require_login
def get_all_posts():
    posts = db.query(Post).all()

    return jsonify(PostSchema().dump(posts, many=True))
