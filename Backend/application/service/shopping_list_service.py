from application.dto.shopping_listDTO import ShoppingListDTO
from application import db
from application.model.models import ShoppingList
from application.repository.shopping_list_repository import ShoppingListRepository


class ShoppingListService:
    @staticmethod
    def create_shopping_list(**data):
        shopping_list_DTO = ShoppingListDTO()
        shopping_list_data = shopping_list_DTO.load(data)

        # daca produsul respectiv se afla deja in lista de cumparaturi a clientului
        # crestem doar numarul de produse - facem update la el
        # daca e un produs nou, il cream si il inseram normal
        shopping_list_exists = ShoppingListRepository.find_shopping_list_by_user_id_and_product_id(
            shopping_list_data.get("id_user"),
            shopping_list_data.get("id_product"))

        if shopping_list_exists:
            number_of_products = shopping_list_exists.get_number_of_products() + shopping_list_data.get(
                "number_of_products")
            shopping_list_exists.number_of_products = number_of_products
            db.session.commit()
            return shopping_list_exists
        else:
            shopping_list_new = ShoppingList(id_user=shopping_list_data.get('id_user'),
                                             id_product=shopping_list_data.get('id_product'),
                                             name_product=shopping_list_data.get('name_product'),
                                             number_of_products=shopping_list_data.get('number_of_products')
                                             )
        return ShoppingListRepository.add_shopping_list(shopping_list_new)

    @staticmethod
    def delete_shopping_list(shopping_list_id):
        shopping_list_exists = ShoppingListRepository.find_shopping_list_by_id(shopping_list_id)
        # daca numarul de produse e mai mare decat 1, se scade valoarea cu 1
        # daca e mai mic sau egal, se sterge din lista de cumparaturi
        if shopping_list_exists.get_number_of_products() > 1:
            number_of_products = shopping_list_exists.get_number_of_products() - 1
            shopping_list_exists.number_of_products = number_of_products
            db.session.commit()
            return shopping_list_exists
        else:
            return ShoppingListRepository.delete_shopping_list(shopping_list_id)

    # stergerea listei de cumparaturi a unui client
    @staticmethod
    def delete_shopping_list_by_user_id(user_id):
        shopping_lists = ShoppingListRepository.delete_shopping_list_by_user_id(user_id)
        if shopping_lists:
            return [shopping_list.repr() for shopping_list in shopping_lists]
        else:
            return "No shopping"

    @staticmethod
    def update_shopping_list(shopping_list_id, data):
        return ShoppingListRepository.update_shopping_list(shopping_list_id, data)

    @staticmethod
    def get_shopping_list_by_id(shopping_list_id):
        return ShoppingListRepository.find_shopping_list_by_id(shopping_list_id)

    # add for logic_project
    @staticmethod
    def find_shopping_list_by_product_name(name_product):
        return ShoppingListRepository.find_shopping_list_by_product_name(name_product)

    # afisarea listei de cumparaturi a unui client
    @staticmethod
    def get_all_shopping_lists_by_user_id(user_id):
        shopping_lists = ShoppingListRepository.find_all_shopping_list_by_user_id(user_id)
        return [shopping_list.repr() for shopping_list in shopping_lists]

    @staticmethod
    def get_all_shopping_lists():
        shopping_lists = ShoppingListRepository.find_all_shopping_list()
        return [shopping_list.repr() for shopping_list in shopping_lists]
