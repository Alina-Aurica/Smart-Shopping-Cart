from marshmallow import fields, Schema, validate

from application.model.role import Role


# dump_only - poate fi citit, dar nu si scris
# required - necesar
class UserDTO(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1))
    # regex de validare a email-ului
    email = fields.Str(required=True, validate=validate.Regexp('^[a-zA-Z0-9_. +-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+$'))
    password = fields.Str(required=True, validate=validate.Length(min=8))
    role = fields.Enum(Role, by_value=True)
