import sys
from flask import request, jsonify
from controllers.utils_controller import check_allowed_keys, check_required_keys
from controllers.errors_controller import errors
from repositories.mongodb_repository import check_if_exists, fields_of_query_param, filters_of_query_param, find_all, find_one, insert_one, replace_one, delete_one


def post_flashcards():
    try:
        data = request.get_json()
        required_allowed_keys = ['question', 'answer', 'category']
        check_required_keys(data, required_allowed_keys)
        data = check_allowed_keys(data, required_allowed_keys)
        id = insert_one('flashcards', data)
        return jsonify(msg="Flashcard successfully registered", id=id), 201
    except Exception as e:
        response = errors(e)
        if response:
            return response
        else:
            return jsonify(msg="Error creating flashcard"), 500


def get_flashcards():
    try:
        query_params = dict(request.args)
        fields = fields_of_query_param(query_params)
        filters = filters_of_query_param(query_params)
        return jsonify(find_all('flashcards', *fields, **filters)), 200
    except Exception as e:
        response = errors(e)
        if response:
            return response
        else:
            return jsonify(msg="Error searching flashcards"), 500


def get_flashcards_id(id):
    try:
        query_params = dict(request.args)
        fields = fields_of_query_param(query_params)
        return jsonify(find_one('flashcards', *fields, id=id)), 200
    except Exception as e:
        response = errors(e)
        if response:
            return response
        else:
            return jsonify(msg="Error searching flashcard"), 500


def put_flashcards_id(id):
    try:
        data = request.get_json()
        required_allowed_keys = ['question', 'answer', 'category']
        check_required_keys(data, required_allowed_keys)
        data = check_allowed_keys(data, required_allowed_keys)
        if not check_if_exists('flashcards', id=id):
            return jsonify(msn='Flashcard not found'), 404
        replace_one('flashcards', data, id=id)
        return jsonify(msg="Flashcard successfully updated"), 200
    except Exception as e:
        response = errors(e)
        if response:
            return response
        else:
            return jsonify(msg="Error updating flashcard"), 500


def delete_flashcards_id(id):
    try:
        if not check_if_exists('flashcards', id=id):
            return jsonify(msn='Flashcard not found'), 404
        delete_one('flashcards', id=id)
        return '', 204
    except Exception as e:
        response = errors(e)
        if response:
            return response
        else:
            return jsonify(msg="Error deleting flashcard"), 500
