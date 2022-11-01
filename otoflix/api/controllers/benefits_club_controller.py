from flask import request, jsonify
from controllers.utils_controller import check_required_keys, check_allowed_keys
from controllers.errors_controller import errors
from repositories.mongodb_repository import check_if_exists, delete_one, fields_of_query_param, filters_of_query_param, find_all, find_one, insert_one, replace_one


def post_benefits_club():
    try:
        data = request.get_json()
        required_allowed_keys = ['benefit_name', 'benefit_description', 'benefit_end_date', 'discount_percentage', 'saved_amount', 'benefit_link']
        check_required_keys(data, required_allowed_keys)
        data = check_allowed_keys(data, required_allowed_keys)
        id = insert_one('benefits_club', data)
        return jsonify(msg="Benefit successfully registered", id=id), 201
    except Exception as e:
        response = errors(e)
        if response:
            return response
        else:
            return jsonify(msg="Error creating benefit"), 500

def get_benefits_club():
    try:
        query_params = dict(request.args)
        fields = fields_of_query_param(query_params)
        filters = filters_of_query_param(query_params)
        return jsonify(find_all('benefits_club', *fields, **filters)), 200
    except Exception as e:
        response = errors(e)
        if response:
            return response
        else:
            return jsonify(msg="Error searching Benefits"), 500


def get_benefits_club_id(id):
    try:
        query_params = dict(request.args)
        fields = fields_of_query_param(query_params)
        return jsonify(find_one('benefits_club', *fields, id=id)), 200
    except Exception as e:
        response = errors(e)
        if response:
            return response
        else:
            return jsonify(msg="Error searching benefit"), 500


def put_benefits_club_id(id):
    try:
        data = request.get_json()
        required_allowed_keys = ['benefit_name', 'benefit_description', 'benefit_end_date', 'discount_percentage', 'saved_amount', 'benefit_link']
        check_required_keys(data, required_allowed_keys)
        data = check_allowed_keys(data, required_allowed_keys)
        if not check_if_exists('benefits_club', id=id):
            return jsonify(msn='Benefit not found'), 404
        replace_one('benefits_club', data, id=id)
        return jsonify(msg="Benefit successfully updated"), 200
    except Exception as e:
        response = errors(e)
        if response:
            return response
        else:
            return jsonify(msg="Error updating benefit"), 500


def delete_benefits_club_id(id):
    try:
        if not check_if_exists('benefits_club', id=id):
            return jsonify(msn='Benefit not found'), 404
        delete_one('benefits_club', id=id)
        return '', 204
    except Exception as e:
        response = errors(e)
        if response:
            return response
        else:
            return jsonify(msg="Error deleting benefit"), 500
