from flask import Blueprint, request, jsonify
from marshmallow import ValidationError

from application.service.user_service import UserService

user_controller = Blueprint('user_controller', __name__, url_prefix='/user')

@user_controller.route('/addUser', methods=['POST'])
def add_user():
    data = request.get_json()
    try:
        user = UserService.create_user(**data)
        return jsonify(user.repr()), 201
    except ValidationError as err:
        return jsonify(err.messages), 400


@user_controller.route('/getUserByID/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    user = UserService.get_user_by_id(user_id)
    return jsonify(user.repr()), 200


@user_controller.route('/getUserByEmail/<string:user_email>', methods=['GET'])
def get_user_by_email(user_email):
    user = UserService.get_user_by_email(user_email)
    return jsonify(user.repr()), 200

