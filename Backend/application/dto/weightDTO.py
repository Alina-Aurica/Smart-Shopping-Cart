from marshmallow import Schema, fields

# dump_only - poate fi citit, dar nu si scris
# required - necesar
class WeightDTO(Schema):
    id = fields.Int(dump_only=True)
    id_user = fields.Int(required=True)
    weight_value = fields.Float(required=True)
    register_at = fields.DateTime(dump_only=True)