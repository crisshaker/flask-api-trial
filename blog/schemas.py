from marshmallow import Schema, fields, EXCLUDE, validates, ValidationError, pre_load


class UserSchema(Schema):
    id = fields.Integer(dump_only=True)
    username = fields.String(required=True)
    password = fields.String(required=True, load_only=True)
    created_at = fields.DateTime(dump_only=True)

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

    class Meta:
        unknown = EXCLUDE


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
