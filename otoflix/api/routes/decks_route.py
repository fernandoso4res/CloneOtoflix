from flask import Blueprint
from flask_jwt_extended import jwt_required
from controllers import decks_controller

bp = Blueprint('decks', __name__)

@bp.route('/', methods=['POST'])
# @jwt_required()
def post_decks():
    return decks_controller.post_decks()

@bp.route('/', methods=['GET'])
def get_decks():
    return decks_controller.get_decks()

@bp.route('/<id>', methods=['GET'])
def get_decks_id(id):
    return decks_controller.get_decks_id(id)

@bp.route('/<id>', methods=['PUT'])
def put_decks_id(id):
    return decks_controller.put_decks_id(id)

@bp.route('/<id>', methods=['DELETE'])
def delete_decks_id(id):
    return decks_controller.delete_decks_id(id)