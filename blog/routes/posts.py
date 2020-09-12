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


@blueprint.route('/', methods=['POST'])
@require_login
def create_post():
    body = request.get_json(force=True)

    title = body.get('title')
    post_body = body.get('body')

    errors = {}
    if not (title and len(title.strip())):
        errors['title'] = 'Title required'

    if not (post_body and len(post_body.strip())):
        errors['body'] = 'Body required'

    if len(errors):
        return jsonify({'errors': errors}), 400

    post = Post(title=title, body=post_body, author_id=g.user.id)
    db.add(post)
    db.commit()

    return jsonify(PostSchema().dump(post))


@blueprint.route('/<id>', methods=['GET'])
@require_login
def get_post(id):
    post = db.query(Post).filter(Post.id == id).first()
    if not post:
        return jsonify({'error': 'Post not found'}), 404

    return jsonify(PostSchema().dump(post))


@blueprint.route('/<id>', methods=['PUT'])
@require_login
def update_post(id):
    body = request.get_json(force=True)

    fields = ['title', 'body']
    update = PostSchema(only=fields).load(body)

    updated = db.query(Post).filter(Post.id == id).update(update)
    db.commit()

    return jsonify({'success': True if updated else False})


@blueprint.route('/<id>', methods=['DELETE'])
@require_login
def delete_post(id):
    deleted = db.query(Post).filter(Post.id == id).delete()
    db.commit()

    return jsonify({'success': True if deleted else False})
