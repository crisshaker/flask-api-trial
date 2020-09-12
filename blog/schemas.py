from marshmallow import Schema, fields, EXCLUDE


class UserSchema(Schema):
    id = fields.Integer()
    username = fields.String()


class PostSchema(Schema):
    id = fields.Integer()
    title = fields.String()
    body = fields.String()
    author_id = fields.Integer()
    author = fields.Nested(UserSchema())
    created_at = fields.DateTime()
    updated_at = fields.DateTime()

    class Meta:
        unknown = EXCLUDE
