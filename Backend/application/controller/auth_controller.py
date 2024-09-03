from flask import Blueprint, request, jsonify
from marshmallow import ValidationError

from application.service.shopping_list_service import ShoppingListService
from application.service.weight_service import WeightService
from application.service.user_service import UserService
from werkzeug.security import check_password_hash

auth_controller = Blueprint('auth_controller', __name__, url_prefix='/auth')

@auth_controller.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email:
        return jsonify({'message': 'Missing email'}), 400
    if not password:
        return jsonify({'message': 'Missing password'}), 400

    user = UserService.get_user_by_email(email)
    # se verifica parola
    if user and check_password_hash(user.password, password):
        return jsonify(user.repr()), 200
    else:
        return jsonify({'message': 'Invalid email or password'}), 400


@auth_controller.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')

    # se verifica unicitatea email-ului
    if UserService.get_user_by_email(email):
        return jsonify({'message': 'User already registered'}), 400

    try:
        user = UserService.create_user(**data)
        return jsonify(user.repr()), 201
    except ValidationError as err:
        return jsonify(err.messages), 400


@auth_controller.route('/logout/<int:user_id>', methods=['DELETE'])
def logout(user_id):
    # se sterge lista de cumparaturi si
    # greutatile aferente sesiunii curente
    # (clientului care se delogheaza)
    shopping_lists = ShoppingListService.delete_shopping_list_by_user_id(user_id)
    weights = WeightService.delete_weight_by_user_id(user_id)
    print(shopping_lists)
    print(weights)
    if shopping_lists and weights:
        return jsonify(shopping_lists), 200
    return jsonify({'message': 'Error - shopping_lists or weights not found'}), 404
