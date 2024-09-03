from marshmallow import Schema, fields, validate

# dump_only - poate fi citit, dar nu si scris
# required - necesar
class ShoppingListDTO(Schema):
    id = fields.Int(dump_only=True)
    id_user = fields.Int(required=True, validate=validate.Range(min=1))
    id_product = fields.Int(required=True, validate=validate.Range(min=1))
    name_product = fields.Str(required=True, validate=validate.Length(min=1))
    number_of_products = fields.Int(required=True, validate=validate.Range(min=1))
    # se pre-initializeaza cu False la creerea obiectului
    recognized = fields.Bool(required=False)
