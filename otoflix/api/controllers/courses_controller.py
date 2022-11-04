import sys
from flask import request, jsonify
from controllers.utils_controller import check_allowed_keys, check_required_keys
from controllers.errors_controller import errors
from controllers.queue_controller import send_to_queue
from repositories.mongodb_repository import check_if_exists, fields_of_query_param, filters_of_query_param, find_all, find_one, insert_one, replace_one, delete_one

def post_courses():
    try:
        data = request.get_json()
        required_allowed_keys = ["name", "description", "image", "teacher_name", "creator", "modules_id"]
        check_required_keys(data, required_allowed_keys)
        data = check_allowed_keys(data, required_allowed_keys)
        id = insert_one('courses', data)
        return jsonify(msg="Course succesfully registered", id=id), 201
    except Exception as e:
        response = errors(e)
        if response:
            return response
        else: 
            return jsonify(msg="Error creating course"), 500

def get_courses():
    try:
        query_params = dict(request.args)
        fields = fields_of_query_param(query_params)
        filters = filters_of_query_param(query_params)
        return jsonify(find_all('courses', *fields, **filters)), 200
    except Exception as e:
        response = errors(e)
        if response:
            return response
        else:
            return jsonify(msg="Error searching courses"), 500

def get_courses_id(id):
    try:
        query_params = dict(request.args)
        fields = fields_of_query_param(query_params)
        return jsonify(find_one('courses', *fields, id=id)), 200
    except Exception as e:
        response = errors(e)
        if response:
            return response
        else:
            return jsonify(msg="Error searching courses"), 500


def put_courses_id(id):
    try:
        data = request.get_json()
        required_allowed_keys = ['name', 'description', 'image', 'teacher_name', 'creator']
        check_required_keys(data, required_allowed_keys)
        data = check_allowed_keys(data, required_allowed_keys)
        if not check_if_exists('courses', id=id):
            return jsonify(msn='Course not found'), 404
        replace_one('courses', data, id=id)
        return jsonify(msg="Course successfully updated"), 200
    except Exception as e:
        response = errors(e)
        if response:
            return response
        else:
            return jsonify(msg="Error updating Course"), 500

def delete_courses_id(id):
    try:
        if not check_if_exists('courses', id=id):
            return jsonify(msn='Course not found'), 404
        delete_one('courses', id=id)
        return jsonify(msg="Curso excluído com sucesso"), 200   
    except Exception as e:
        response = errors(e)
        if response:
            return response
        else:
            return jsonify(msg="Error deleting course"), 500