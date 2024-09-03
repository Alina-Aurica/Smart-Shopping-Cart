from flask import Blueprint, request, jsonify
from marshmallow import ValidationError

from application.service.product_service import ProductService

product_controller = Blueprint('product_controller', __name__, url_prefix='/product')

@product_controller.route('/addProduct', methods=['POST'])
def add_product():
    data = request.get_json()
    try:
        product = ProductService.create_product(**data)
        return jsonify(product.repr()), 201
    except ValidationError as err:
        return jsonify(err.messages), 400


@product_controller.route('/updateProduct/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    data = request.get_json()
    product = ProductService.update_product(product_id, data)
    if product:
        return jsonify(product.repr()), 200
    return jsonify({'message': 'Error - product not found'}), 404


@product_controller.route('/deleteProduct/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    product = ProductService.delete_product(product_id)
    if product:
        return jsonify(product.repr()), 200
    return jsonify({'message': 'Error - product not found'}), 404


@product_controller.route('/getProductById/<int:product_id>', methods=['GET'])
def get_product_by_id(product_id):
    product = ProductService.get_product_by_id(product_id)
    return jsonify(product.repr()), 200


@product_controller.route('/getProductByName/<string:product_name>', methods=['GET'])
def get_product_by_name(product_name):
    product = ProductService.get_product_by_name(product_name)
    return jsonify(product.repr()), 200


@product_controller.route('/getAllProducts', methods=['GET'])
def get_all_products():
    products = ProductService.get_all_products()
    return jsonify(products), 200
