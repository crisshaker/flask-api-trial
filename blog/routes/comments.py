from flask import Blueprint, request, jsonify, g
from blog.database import db
from blog.models import Comment
from blog.schemas import CommentSchema
from blog.decorators import require_login, owns_comment

blueprint = Blueprint('comments', __name__)


@blueprint.route('/comments/<id>', methods=['PUT'])
@require_login
@owns_comment
def update_comment(id):
    body = request.get_json(force=True)

    update = CommentSchema().load(body)
    updated = db.query(Comment).filter(
        Comment.id == id, Comment.author_id == g.user.id).update(update)
    db.commit()

    return jsonify({'success': True if updated else False})


@blueprint.route('/comments/<id>', methods=['DELETE'])
@require_login
@owns_comment
def delete_comment(id):
    deleted = db.query(Comment).filter(
        Comment.id == id, Comment.author_id == g.user.id).delete()
    db.commit()

    return jsonify({'success': True if deleted else False})
