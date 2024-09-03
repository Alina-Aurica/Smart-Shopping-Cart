from flask import Blueprint, request, jsonify
from marshmallow import ValidationError

from application.service.shopping_list_service import ShoppingListService

shopping_list_controller = Blueprint('shopping_list_controller', __name__, url_prefix='/shoppinglist')

@shopping_list_controller.route('/addShoppingList', methods=['POST'])
def add_shopping_list():
    data = request.get_json()
    try:
        shopping_list = ShoppingListService.create_shopping_list(**data)
        return jsonify(shopping_list.repr()), 201
    except ValidationError as err:
        return jsonify(err.messages), 400


@shopping_list_controller.route('/updateShoppingList/<int:shopping_list_id>', methods=['PUT'])
def update_shopping_list(shopping_list_id):
    data = request.get_json()
    shopping_list = ShoppingListService.update_shopping_list(shopping_list_id, data)
    if shopping_list:
        return jsonify(shopping_list.repr()), 200
    return jsonify({'message': 'Error - shopping_list not found'}), 404

# folosit pentru aa sterge produse din lista de cumparaturi
@shopping_list_controller.route('/deleteShoppingList/<int:shopping_list_id>', methods=['DELETE'])
def delete_shopping_list(shopping_list_id):
    shopping_list = ShoppingListService.delete_shopping_list(shopping_list_id)
    if shopping_list:
        return jsonify(shopping_list.repr()), 200
    return jsonify({'message': 'Error - shopping_list not found'}), 404

@shopping_list_controller.route('/deleteShoppingListByUserId/<int:user_id>', methods=['DELETE'])
def delete_shopping_list_by_user_id(user_id):
    shopping_lists = ShoppingListService.delete_shopping_list_by_user_id(user_id)
    if shopping_lists:
        return jsonify(shopping_lists), 200
    return jsonify({'message': 'Error - shopping_lists not found'}), 404


@shopping_list_controller.route('/getShoppingListById/<int:shopping_list_id>', methods=['GET'])
def get_shopping_list_by_id(shopping_list_id):
    shopping_list = ShoppingListService.get_shopping_list_by_id(shopping_list_id)
    return jsonify(shopping_list.repr()), 200

# returneaza lista de cumparaturi a unui client
@shopping_list_controller.route('/getAllShoppingListsByUserId/<int:user_id>', methods=['GET'])
def get_all_shopping_lists_by_user_id(user_id):
    shopping_lists = ShoppingListService.get_all_shopping_lists_by_user_id(user_id)
    return jsonify(shopping_lists), 200


@shopping_list_controller.route('/getAllShoppingLists', methods=['GET'])
def get_all_shopping_lists():
    shopping_lists = ShoppingListService.get_all_shopping_lists()
    return jsonify(shopping_lists), 200
