from sqlalchemy import func

from application import db
from application.model.models import ShoppingList

# db.session.add() - adaugare in baza de date
# db.session.delete() - stergere din baza de date
# db.session.commit() - salvarea schimbarilor in baza de date
# query - pentru interogari de tip SELECT... FROM... WHERE...
class ShoppingListRepository:
    @staticmethod
    def add_shopping_list(shopping_list):
        db.session.add(shopping_list)
        db.session.commit()
        return shopping_list

    @staticmethod
    def delete_shopping_list(shopping_list_id):
        shopping_list = ShoppingList.query.get(shopping_list_id)
        if shopping_list:
            db.session.delete(shopping_list)
            db.session.commit()
            return shopping_list
        return None

    # folosit pentru logOut
    # pentru ca shopping list-ul clientului
    # sa se stearga la final
    @staticmethod
    def delete_shopping_list_by_user_id(user_id):
        shopping_lists = ShoppingList.query.filter_by(id_user=user_id).all()
        if shopping_lists:
            for shopping_list in shopping_lists:
                db.session.delete(shopping_list)
                db.session.commit()
            return shopping_lists
        return None

    @staticmethod
    def update_shopping_list(shopping_list_id, data):
        shopping_list = ShoppingList.query.get(shopping_list_id)
        if shopping_list:
            shopping_list.id_user = data.get('id_user', shopping_list.id_user)
            shopping_list.id_product = data.get('id_product', shopping_list.id_product)
            shopping_list.name_product = data.get('name_product', shopping_list.name_product)
            shopping_list.number_of_products = data.get('number_of_products', shopping_list.number_of_products)
            db.session.commit()
        return shopping_list

    @staticmethod
    def find_shopping_list_by_id(shopping_list_id):
        return ShoppingList.query.get(shopping_list_id)

    # folosit in logic_project
    # pentru ca cauta eticheta generata de inferente
    # in denumirea produselor
    @staticmethod
    def find_shopping_list_by_product_name(name_product):
        return ShoppingList.query.filter(func.lower(ShoppingList.name_product).like(f"%{name_product.lower()}%")).first()

    # returneaza lista de cumparaturi a unui client
    @staticmethod
    def find_all_shopping_list_by_user_id(user_id):
        return ShoppingList.query.filter_by(id_user=user_id).all()

    @staticmethod
    def find_shopping_list_by_user_id_and_product_id(user_id, product_id):
        return ShoppingList.query.filter_by(id_user=user_id, id_product=product_id).first()

    @staticmethod
    def find_all_shopping_list():
        return ShoppingList.query.all()
