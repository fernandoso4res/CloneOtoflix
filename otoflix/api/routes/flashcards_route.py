from flask import Blueprint
from flask_jwt_extended import jwt_required
from controllers import flashcards_controller

bp = Blueprint('flashcards', __name__)

@bp.route('/', methods=['POST'])
@jwt_required()
def post_flashcards():
    return flashcards_controller.post_flashcards()

@bp.route('/', methods=['GET'])
@jwt_required()
def get_flashcards():
    return flashcards_controller.get_flashcards()

@bp.route('/<id>', methods=['GET'])
def get_flashcards_id(id):
    return flashcards_controller.get_flashcards_id(id)

@bp.route('/<id>', methods=['PUT'])
@jwt_required()
def put_flashcards_id(id):
    return flashcards_controller.put_flashcards_id(id)

@bp.route('/<id>', methods=['DELETE'])
@jwt_required()
def delete_flashcards_id(id):
    return flashcards_controller.delete_flashcards_id(id)