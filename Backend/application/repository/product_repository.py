from application import db
from application.model.models import Product


# db.session.add() - adaugare in baza de date
# db.session.delete() - stergere din baza de date
# db.session.commit() - salvarea schimbarilor in baza de date
# query - pentru interogari de tip SELECT... FROM... WHERE...
class ProductRepository:
    @staticmethod
    def add_product(product):
        db.session.add(product)
        db.session.commit()
        return product

    @staticmethod
    def delete_product(product_id):
        product = Product.query.get(product_id)
        if product:
            db.session.delete(product)
            db.session.commit()
            return product
        return None

    @staticmethod
    def update_product(product_id, data):
        product = Product.query.get(product_id)
        if product:
            product.name = data.get('name', product.name)
            product.quantity_min = data.get('quantity_min', product.quantity_min)
            product.quantity_max = data.get('quantity_max', product.quantity_max)
            product.stock = data.get('stock', product.stock)
            product.image_url = data.get('image_url', product.image_url)
            db.session.commit()
        return product

    @staticmethod
    def find_product_by_id(product_id):
        return Product.query.get(product_id)

    @staticmethod
    def find_product_by_name(product_name):
        return Product.query.filter_by(name=product_name).first()

    @staticmethod
    def find_all_products():
        return Product.query.all()
