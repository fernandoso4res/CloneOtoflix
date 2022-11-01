from flask import Blueprint
from flask_jwt_extended import jwt_required
from controllers import rankings_controller

bp = Blueprint('rankings', __name__)

@bp.route('/', methods=['GET'])
@jwt_required()
def get_rankings():
    return rankings_controller.get_rankings()
