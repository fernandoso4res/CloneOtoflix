from flask import Blueprint
from flask_jwt_extended import jwt_required
from controllers import benefits_club_controller

bp = Blueprint('benefits_club', __name__)

@bp.route('/', methods=['POST'])
def post_benefits_club():
    return benefits_club_controller.post_benefits_club()

@bp.route('/', methods=['GET'])
def get_benefits_club():
    return benefits_club_controller.get_benefits_club()

@bp.route('/<id>', methods=['GET'])
def get_benefits_club_id(id):
    return benefits_club_controller.get_benefits_club_id(id)

@bp.route('/<id>', methods=['PUT'])
def put_benefits_club_id(id):
    return benefits_club_controller.put_benefits_club_id(id)

@bp.route('/<id>', methods=['DELETE'])
def delete_benefits_club_id(id):
    return benefits_club_controller.delete_benefits_club_id(id)