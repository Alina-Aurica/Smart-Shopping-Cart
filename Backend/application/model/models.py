from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Enum

from application.model.role import Role

# initializarea bazei de date
db = SQLAlchemy()

# clasa User
# cheie primara: id
# email - unic
# role - initializat cu CLIENT
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    role = db.Column(Enum(Role, name='role', create_type=False), default=Role.CLIENT)

    def repr(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "role": self.role.name
        }

# clasa Product
# cheie primara> id
class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    quantity_min = db.Column(db.Float(), nullable=False)
    quantity_max = db.Column(db.Float(), nullable=False)
    stock = db.Column(db.Integer(), nullable=False)
    image_url = db.Column(db.String(), nullable=False)

    def repr(self):
        return {
            "id": self.id,
            "name": self.name,
            "quantity_min": self.quantity_min,
            "quantity_max": self.quantity_max,
            "stock": self.stock,
            "image_url": self.image_url
        }


# clasa ShoppingList
# cheie primara: id
# chei straine: id_user, id_product
# recognised - initializat cu False
class ShoppingList(db.Model):
    __tablename__ = 'shoppinglists'

    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    id_product = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    name_product = db.Column(db.String, nullable=False)
    number_of_products = db.Column(db.Integer(), nullable=False)
    recognised = db.Column(db.Boolean(), default=False)

    def get_number_of_products(self):
        return self.number_of_products

    def repr(self):
        return {
            "id": self.id,
            "id_user": self.id_user,
            "id_product": self.id_product,
            "name_product": self.name_product,
            "number_of_products": self.number_of_products,
            "recognised": self.recognised
        }

# clasa Weight
# cheie primara: id
# cheie straina: id_user
# register_at - initializat cu data si timpul curent
class Weight(db.Model):
    __tablename__ = 'weights'

    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    weight_value = db.Column(db.Float, nullable=False)
    register_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def repr(self):
        return {
            "id": self.id,
            "id_user": self.id_user,
            "weight_value": self.weight_value,
            "register_at": self.register_at
        }
