from flask import Blueprint
from flask_jwt_extended import jwt_required
from controllers import questions_controller

bp = Blueprint('questions', __name__)


@bp.route('/', methods=['GET'])
def get_questions():
    return questions_controller.get_questions()

@bp.route('/multiple-choice-question', methods=['POST'])
# @jwt_required()
def post_multiple_choice_question():
    return questions_controller.post_questions(type='multiple_choice_question')

@bp.route('/open-question', methods=['POST'])
# @jwt_required()
def post_open_question():
    return questions_controller.post_questions(type='open_question')











@bp.route('/<id>', methods=['GET'])
def get_questions_id(id):
    return questions_controller.get_questions_id(id)

@bp.route('/<id>', methods=['PUT'])
# @jwt_required()
def put_questions_id(id):
    return questions_controller.put_questions_id(id)

@bp.route('/<id>', methods=['DELETE'])
# @jwt_required()
def delete_questions_id(id):
    return questions_controller.delete_questions_id(id)