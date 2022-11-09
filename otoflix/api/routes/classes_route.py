from flask import Blueprint
from flask_jwt_extended import jwt_required
from controllers import classes_controller

bp = Blueprint('classes', __name__)

@bp.route('/', methods=['POST'])
#@jwt_required()
def post_classes():
    return classes_controller.post_classes()

def get_classes():
    return classes_controller.get_classes()

@bp.route('/<id>', methods=['GET'])
def get_classes_id(id):
    return classes_controller.get_classes_id(id)

@bp.route('/<id>', methods=['PUT'])
#@jwt_required()
def put_classes_id(id):
    return classes_controller.put_classes_id(id)

@bp.route('/<id>', methods=['DELETE'])
#@jwt_required()
def delete_classes_id(id):
    return classes_controller.delete_classes_id(id)