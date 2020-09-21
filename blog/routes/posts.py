from flask import Blueprint, jsonify, request, abort, g
from blog.database import db
from blog.models import Post, Comment
from blog.schemas import PostSchema, CommentSchema
from blog.decorators import require_login, owns_post, owns_comment

blueprint = Blueprint('posts', __name__)


@blueprint.route('/posts', methods=['GET'])
def get_all_posts():
    posts = db.query(Post).all()
    return jsonify(PostSchema().dump(posts, many=True))


@blueprint.route('/posts', methods=['POST'])
@require_login
def create_post():
    body = request.get_json(force=True)

    data = PostSchema(only=['post', 'title']).load(body)
    post = Post(**data, author_id=g.user.id)
    db.add(post)
    db.commit()

    return jsonify(PostSchema().dump(post))


@blueprint.route('/posts/<id>', methods=['GET'])
def get_post(id):
    post = db.query(Post).filter(Post.id == id).first()
    if not post:
        return jsonify({'error': 'Post not found'}), 404

    return jsonify(PostSchema().dump(post))


@blueprint.route('/posts/<id>', methods=['PUT'])
@require_login
@owns_post
def update_post(id):
    body = request.get_json(force=True)

    update = PostSchema(only=['title', 'body']).load(body)
    updated = db.query(Post).filter(
        Post.id == id, Post.author_id == g.user.id).update(update)
    db.commit()

    return jsonify({'success': True if updated else False})


@blueprint.route('/posts/<id>', methods=['DELETE'])
@require_login
@owns_post
def delete_post(id):
    deleted = db.query(Post).filter(
        Post.id == id, Post.author_id == g.user.id).delete()
    db.commit()

    return jsonify({'success': True if deleted else False})


@blueprint.route('/posts/<id>/comments', methods=['GET'])
def get_post_comments(id):
    comments = db.query(Comment).filter(Comment.post_id == id).all()
    return jsonify(CommentSchema().dump(comments, many=True))


@blueprint.route('/posts/<id>/comments', methods=['POST'])
@require_login
def comment_on_post(id):
    body = request.get_json(force=True)

    data = CommentSchema(only=['body']).load(body)
    comment = Comment(**data, author_id=g.user.id, post_id=id)
    db.add(comment)
    db.commit()

    return jsonify(CommentSchema().dump(comment))
