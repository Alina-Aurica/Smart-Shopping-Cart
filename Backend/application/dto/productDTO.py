from marshmallow import Schema, fields, validate

# dump_only - poate fi citit, dar nu si scris
# required - necesar
class ProductDTO(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1))
    quantity_min = fields.Float(required=True)
    quantity_max = fields.Float(required=True)
    stock = fields.Int(required=True)
    image_url = fields.Str(required=True, validate=validate.Length(min=1))
