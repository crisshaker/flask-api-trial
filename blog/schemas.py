from marshmallow import Schema, fields, EXCLUDE, validates, ValidationError, pre_load


class UserSchema(Schema):
    id = fields.Integer()
    username = fields.String(required=True)
    password = fields.String(required=True, load_only=True)
    created_at = fields.DateTime()

    class Meta:
        unknown = EXCLUDE

    @pre_load
    def pre_load(self, data, **kwargs):
        if 'username' in data:
            data['username'] = data['username'].strip().lower()

        return data

    @validates('username')
    def validate_username(self, value):
        if len(value) < 5:
            raise ValidationError(
                'Username must be at least 5 characters long')

    @validates('password')
    def validate_password(self, value):
        if len(value) < 6:
            raise ValidationError(
                'Password must be at least 6 characters long')


class PostSchema(Schema):
    id = fields.Integer()
    title = fields.String(required=True)
    body = fields.String(required=True)
    author_id = fields.Integer()
    author = fields.Nested(UserSchema())
    created_at = fields.DateTime()
    updated_at = fields.DateTime()

    class Meta:
        unknown = EXCLUDE

    @pre_load
    def pre_load(self, data, **kwargs):
        for field in ['title', 'body']:
            if field in data:
                data[field] = data[field].strip()

        return data

    @validates('title')
    def validate_title(self, value):
        if len(value) == 0:
            raise ValidationError('Title cannot be empty')

    @validates('body')
    def validate_body(self, value):
        if len(value) == 0:
            raise ValidationError('Body cannot be empty')


class CommentSchema(Schema):
    id = fields.Integer()
    body = fields.String(required=True)
    author_id = fields.Integer()
    post_id = fields.Integer()
    author = fields.Nested(UserSchema())
    created_at = fields.DateTime()
    updated_at = fields.DateTime()

    class Meta:
        unknown = EXCLUDE

    @pre_load
    def pre_load(self, data, **kwargs):
        if 'body' in data:
            data['body'] = data['body'].strip()

        return data

    @validates('body')
    def validate_body(self, value):
        if len(value) == 0:
            raise ValidationError('Comment body cannot be empty')
