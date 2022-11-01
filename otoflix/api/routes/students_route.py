from flask import Blueprint
from flask_jwt_extended import jwt_required
from controllers import students_controller

bp = Blueprint('students', __name__)


@bp.route('/add-points', methods=['POST'])
@jwt_required()
def post_add_points():
    return students_controller.post_add_points()


@bp.route('/add-points-by-id', methods=['POST'])
@jwt_required()
def post_add_points_by_id():
    return students_controller.post_add_points_by_id()

@bp.route('/get', methods=['GET'])
def get(self):
    return