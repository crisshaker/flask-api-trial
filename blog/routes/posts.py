from flask import Blueprint, jsonify, request, abort, g
from blog.database import db
from blog.models import Post
from blog.schemas import PostSchema
from blog.decorators import require_login, owns_post

blueprint = Blueprint('posts', __name__, url_prefix='/posts')


@blueprint.route('/', methods=['GET'])
@require_login
def get_all_posts():
    posts = db.query(Post).filter(Post.author_id == g.user.id).all()
    return jsonify(PostSchema().dump(posts, many=True))


@blueprint.route('/', methods=['POST'])
@require_login
def create_post():
    body = request.get_json(force=True)

    data = PostSchema().load(body)
    post = Post(**data, author_id=g.user.id)
    db.add(post)
    db.commit()

    return jsonify(PostSchema().dump(post))


@blueprint.route('/<id>', methods=['GET'])
@require_login
@owns_post
def get_post(id):
    post = db.query(Post).filter(
        Post.id == id, Post.author_id == g.user.id).first()
    if not post:
        return jsonify({'error': 'Post not found'}), 404

    return jsonify(PostSchema().dump(post))


@blueprint.route('/<id>', methods=['PUT'])
@require_login
@owns_post
def update_post(id):
    body = request.get_json(force=True)

    fields = ['title', 'body']
    update = PostSchema(only=fields).load(body)
    updated = db.query(Post).filter(Post.id == id).update(update)
    db.commit()

    return jsonify({'success': True if updated else False})


@blueprint.route('/<id>', methods=['DELETE'])
@require_login
@owns_post
def delete_post(id):
    deleted = db.query(Post).filter(
        Post.id == id, Post.author_id == g.user.id).delete()
    db.commit()

    return jsonify({'success': True if deleted else False})
