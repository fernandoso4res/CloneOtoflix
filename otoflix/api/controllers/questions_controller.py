import sys
from flask import request, jsonify
from controllers.utils_controller import check_allowed_keys, check_required_keys
from controllers.errors_controller import errors
from controllers.queue_controller import send_to_queue
from repositories.mongodb_repository import check_if_exists, fields_of_query_param, filters_of_query_param, find_all, find_one, insert_one, replace_one, delete_one


def post_questions(type):
    try:
        data = request.get_json()
        required_allowed_keys = None
        if type == 'multiple_choice_question':
            required_allowed_keys = ['category', 'question', 'correct_answer', 'explanation', 'choices']
        elif type == 'open_question':
            required_allowed_keys = ['category', 'question']
        else:
            return jsonify(msg="Error creating question"), 400
        check_required_keys(data, required_allowed_keys)
        data = check_allowed_keys(data, required_allowed_keys)
        data['question_type'] = type
        id = insert_one('questions', data)
        return jsonify(msg="Question successfully registered", id=id), 201
    except Exception as e:
        response = errors(e)
        if response:
            return response
        else:
            return jsonify(msg="Error creating question"), 500


def get_questions():
    try:
        query_params = dict(request.args)
        fields = fields_of_query_param(query_params)
        filters = filters_of_query_param(query_params)
        return jsonify(find_all('questions', *fields, **filters)), 200
    except Exception as e:
        response = errors(e)
        if response:
            return response
        else:
            return jsonify(msg="Error searching questions"), 500


def get_questions_id(id):
    try:
        query_params = dict(request.args)
        fields = fields_of_query_param(query_params)
        return jsonify(find_one('questions', *fields, id=id)), 200
    except Exception as e:
        response = errors(e)
        if response:
            return response
        else:
            return jsonify(msg="Error searching question"), 500


def put_questions_id(id):
    try:
        data = request.get_json()
        required_allowed_keys = None
        if 'question_type' in data and (data['question_type'] == 'multiple_choice_question' or data['question_type'] == 'open_question'):
            type = data['question_type']
        else:
            raise KeyError('Error - question_type')
        if type == 'multiple_choice_question':
            required_allowed_keys = ['category', 'question', 'correct_answer', 'explanation', 'choices', 'question_type']
        elif type == 'open_question':
            required_allowed_keys = ['category', 'question', 'question_type']
        else:
            return jsonify(msg="Error updating question"), 400
        check_required_keys(data, required_allowed_keys)
        data = check_allowed_keys(data, required_allowed_keys)
        if not check_if_exists('questions', id=id):
            return jsonify(msn='Question not found'), 404
        replace_one('questions', data, id=id)
        return jsonify(msg="Question successfully updated"), 200
    except Exception as e:
        response = errors(e)
        if response:
            return response
        else:
            return jsonify(msg="Error updating question"), 500


def delete_questions_id(id):
    try:
        if not check_if_exists('questions', id=id):
            return jsonify(msn='Question not found'), 404
        delete_one('questions', id=id)
        return '', 204
    except Exception as e:
        response = errors(e)
        if response:
            return response
        else:
            return jsonify(msg="Error deleting question"), 500
