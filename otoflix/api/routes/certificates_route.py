from flask import Blueprint, render_template
from flask_jwt_extended import jwt_required
from controllers import certificates_controller

bp = Blueprint('certificates', __name__)

@bp.route('/', methods=['GET'])
@jwt_required()
def get_certificates():
    return certificates_controller.get_certificates()

