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