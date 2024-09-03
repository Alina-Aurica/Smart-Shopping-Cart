from flask import Blueprint, jsonify

from application.raspberry.hardware_logic import logic_project, close_servo
from application.raspberry.infereceUsingCamera import run_inference

inference_controller = Blueprint('inference_controller', __name__, url_prefix='/inference')


@inference_controller.route('/runInference/<int:user_id>', methods=['GET'])
def start_inference(user_id):
    # eticheta returnata de motorul de inferente
    label = run_inference()
    # verificam daca eticheta apartine unui produs din lista de cumparaturi
    shopping_list = logic_project(label, user_id)
    if shopping_list == "Too many/less products":
        return jsonify(shopping_list), 201
    if shopping_list == "No product found":
        return jsonify(shopping_list), 201
    return jsonify(shopping_list.repr()), 201

# in situatia in care produsul exista in cos,
# dar greutatea nu se potriveste
# se apeleaza aceasta metoda de inchidere a capacului cosului
# dupa ce se asteapta ca produsul incorect sa fie scos din cos
@inference_controller.route("/closeServo", methods=['GET'])
def close_servos():
    print("Ajunge in servo close!")
    if close_servo():
        return jsonify("Works!"), 201
    else:
        return jsonify("Error!"), 404