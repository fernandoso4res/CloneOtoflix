import sys
from flask import request, jsonify
from controllers.utils_controller import check_allowed_keys, check_required_keys
from controllers.errors_controller import errors
from repositories.mongodb_repository import check_if_exists, fields_of_query_param, filters_of_query_param, find_all, find_one, insert_one, replace_one, delete_one


def post_simulated():
    try:
        data = request.get_json()
        required_allowed_keys = ['title', 'questions', 'duration']
        check_required_keys(data, required_allowed_keys)
        data = check_allowed_keys(data, required_allowed_keys)
        categories = []
        for  question in data['questions']:
            category = find_one('questions', 'category', id=question['id'])
            if not category:
                raise KeyError ('Question Id')
            categories.append(category['category'])
        categories = sorted(set(categories))
        data['categories'] = categories
        id = insert_one('simulated', data)
        return jsonify(msg="Simulated successfully registered", id=id), 201
    except Exception as e:
        response = errors(e)
        if response:
            return response
        else:
            return jsonify(msg="Error creating simulated"), 500


def get_simulated():
    try:
        query_params = dict(request.args)
        fields = fields_of_query_param(query_params)
        filters = filters_of_query_param(query_params)
        return jsonify(find_all('simulated', *fields, **filters)), 200
    except Exception as e:
        response = errors(e)
        if response:
            return response
        else:
            return jsonify(msg="Error searching simulated"), 500


def get_simulated_id(id):
    try:
        query_params = dict(request.args)
        fields = fields_of_query_param(query_params)
        return jsonify(find_one('simulated', *fields, id=id)), 200
    except Exception as e:
        response = errors(e)
        if response:
            return response
        else:
            return jsonify(msg="Error searching simulated"), 500


def put_simulated_id(id):
    try:
        data = request.get_json()
        required_allowed_keys = ['title', 'questions', 'duration']
        check_required_keys(data, required_allowed_keys)
        data = check_allowed_keys(data, required_allowed_keys)
        if not check_if_exists('simulated', id=id):
            return jsonify(msn='Simulated not found'), 404
        categories = []
        for  question in data['questions']:
            category = find_one('questions', 'category', id=question['id'])
            if not category:
                raise KeyError ('Question Id')
            categories.append(category['category'])
        categories = sorted(set(categories))
        data['categories'] = categories
        replace_one('simulated', data, id=id)
        return jsonify(msg="Simulated successfully updated"), 200
    except Exception as e:
        response = errors(e)
        if response:
            return response
        else:
            return jsonify(msg="Error updating simulated"), 500


def delete_simulated_id(id):
    try:
        if not check_if_exists('simulated', id=id):
            return jsonify(msn='Simulated not found'), 404
        delete_one('simulated', id=id)
        return '', 204
    except Exception as e:
        response = errors(e)
        if response:
            return response
        else:
            return jsonify(msg="Error deleting simulated"), 500
