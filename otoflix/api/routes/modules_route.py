from flask import Blueprint
from flask_jwt_extended import jwt_required
from controllers import modules_controller

bp = Blueprint('modules', __name__)

@bp.route('/', methods=['POST'])
#@jwt_required()
def post_modules():
    return modules_controller.post_modules()

@bp.route('/', methods=['GET'])
#@jwt_required()
def get_modules():
    return modules_controller.get_modules()

@bp.route('/<id>', methods=['GET'])
def get_modules_id(id):
    return modules_controller.get_modules_id(id)

@bp.route('/<id>', methods=['PUT'])
#@jwt_required()
def put_modules_id(id):
    return modules_controller.put_modules_id(id)

@bp.route('/<id>', methods=['DELETE'])
#@jwt_required()
def delete_modules_id(id):
    return modules_controller.delete_modules_id(id)