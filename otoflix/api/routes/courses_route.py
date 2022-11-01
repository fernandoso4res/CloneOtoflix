from flask import Blueprint
from flask_jwt_extended import jwt_required
from controllers import courses_controller

bp = Blueprint('courses', __name__)

@bp.route('/', methods=['POST'])
#@jwt_required()
def post_courses():
    return courses_controller.post_courses()

@bp.route('/', methods=['GET'])
#@jwt_required()
def get_courses():
    return courses_controller.get_courses()

@bp.route('/<id>', methods=['GET'])
def get_courses_id(id):
    return courses_controller.get_courses_id(id)

@bp.route('/<id>', methods=['PUT'])
#@jwt_required()
def put_courses_id(id):
    return courses_controller.put_courses_id(id)

@bp.route('/<id>', methods=['DELETE'])
#@jwt_required()
def delete_courses_id(id):
    return courses_controller.delete_courses_id(id)