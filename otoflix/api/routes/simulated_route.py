from flask import Blueprint
from flask_jwt_extended import jwt_required
from controllers import simulated_controller

bp = Blueprint('simulated', __name__)

@bp.route('/', methods=['POST'])
# @jwt_required()
def post_simulated():
    return simulated_controller.post_simulated()

@bp.route('/', methods=['GET'])
def get_simulated():
    return simulated_controller.get_simulated()

@bp.route('/<id>', methods=['GET'])
def get_simulated_id(id):
    return simulated_controller.get_simulated_id(id)

@bp.route('/<id>', methods=['PUT'])
# @jwt_required()
def put_simulated_id(id):
    return simulated_controller.put_simulated_id(id)

@bp.route('/<id>', methods=['DELETE'])
# @jwt_required()
def delete_simulated_id(id):
    return simulated_controller.delete_simulated_id(id)