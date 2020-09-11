from marshmallow import Schema, fields


class UserSchema(Schema):
    id = fields.Integer()
    username = fields.String()


class PostSchema(Schema):
    id = fields.Integer()
    title = fields.String()
    body = fields.String()
    user_id = fields.Integer()
