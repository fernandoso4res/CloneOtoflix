from flask import Blueprint
from flask_jwt_extended import jwt_required
from controllers import users_controller

bp = Blueprint('users', __name__)

@bp.route('/', methods=['GET'])
def get_users():
    return users_controller.get_users()

@bp.route('/', methods=['DELETE'])
def delete_users():
    return users_controller.delete_users()

@bp.route('/<id>', methods=['GET'])
def get_users_id(id):
    return users_controller.get_users_id(id)

@bp.route('/<id>', methods=['DELETE'])
def delete_users_id(id):
    return users_controller.delete_users_id(id)

@bp.route('/count', methods=['GET'])
def get_count():
    return users_controller.get_count()

@bp.route('/activate-deactivate', methods=['PATCH'])
def patch_activate_deactivate():
    return users_controller.patch_activate_deactivate()

@bp.route('/profile-picture', methods=['PATCH'])
@jwt_required()
def patch_profile_picture():
    return users_controller.patch_profile_picture()

@bp.route('/profile-infos', methods=['PATCH'])
@jwt_required()
def patch_profile_infos():
    return users_controller.patch_profile_infos()
