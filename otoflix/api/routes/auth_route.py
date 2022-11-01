from flask import Blueprint
from flask_jwt_extended import jwt_required
from controllers import auth_controller

bp = Blueprint('auth', __name__)


@bp.route('/register-student', methods=['POST'])
def register_student():
    return auth_controller.register_user(type='student')


@bp.route('/register-teacher', methods=['POST'])
def register_teacher():
    return auth_controller.register_user(type='teacher')


@bp.route('/register-administrator', methods=['POST'])
def register_administrator():
    return auth_controller.register_user(type='administrator')


@bp.route('/login', methods=['POST'])
def login():
    return auth_controller.login()

@bp.route('/logout', methods=['DELETE'])
@jwt_required()
def logout():
    return auth_controller.logout()

@bp.route("/teste", methods=["GET"])
@jwt_required()
def teste():
    return auth_controller.teste()

@bp.route('/change-password', methods=['PUT'])
@jwt_required()
def change_password():
    return auth_controller.change_password()


@bp.route('/forgot-password-send-token', methods=['POST'])
def forgot_password_send_token():
    return auth_controller.forgot_password_send_token()


@bp.route('/forgot-password-validate-token', methods=['POST'])
def forgot_password_validate_token():
    return auth_controller.forgot_password_validate_token()


@bp.route('/forgot-password-change-password', methods=['POST'])
def forgot_password_change_password():
    return auth_controller.forgot_password_change_password()
