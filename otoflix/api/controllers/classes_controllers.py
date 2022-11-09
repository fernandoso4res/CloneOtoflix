import sys                 
from flask import request, jsonify
from controllers.utils_controller import check_allowed_keys, check_required_keys
from controllers.errors_controller import errors
from controllers.queue_controller import send_to_queue
from repositories.mongodb_repository import check_if_exists, fields_of_query_param, filters_of_query_param, find_all, find_one, insert_one, replace_one, delete_one

def post_classes():
    try:
        data = request.get_json()
        required_allowed_keys = ["name", "duration", "comments", "link_video"]
        check_required_keys(data, required_allowed_keys)
        data = check_allowed_keys(data, required_allowed_keys)
        id = insert_one('classes', data)
        return jsonify(msg="Class succesfully registered", id=id), 201
    except Exception as e:
        response = errors(e)
        if response:
            return response
        else:  
            return jsonify(msg="Error creating class"), 500

def get_classes():
    try:
        query_params = dict(request.args)
        fields = fields_of_query_param(query_params)
        filters = filters_of_query_param(query_params)
        return jsonify(find_all('classes', *fields, **filters)), 200
    except Exception as e:
        response = errors(e)
        if response:
            return response
        else:
            return jsonify(msg="Error searching classes"), 500


def get_classes_id(id):
    try:
        query_params = dict(request.args)
        fields = fields_of_query_param(query_params)
        return jsonify(find_one('classes', *fields, id=id)), 200
    except Exception as e:
        response = errors(e)
        if response:
            return response
        else:
            return jsonify(msg="Error searching classes"), 500


def put_classes_id(id):
    try:
        data = request.get_json()
        required_allowed_keys = ["name", "duration", "comments", "link_video"]
        check_required_keys(data, required_allowed_keys)
        data = check_allowed_keys(data, required_allowed_keys)
        if not check_if_exists('classes', id=id):
            return jsonify(msn='Class not found'), 404
        replace_one('classes', data, id=id)
        return jsonify(msg="Class successfully updated"), 200
    except Exception as e:
        response = errors(e)
        if response:
            return response
        else:
            return jsonify(msg="Error updating class"), 500



def delete_class_id(id):
    try:
        if not check_if_exists('classes', id=id):
            return jsonify(msn='Class not found'), 404
        delete_one('classes', id=id)
        return jsonify(msg="Aula excluída com sucesso"), 200   
    except Exception as e:
        response = errors(e)
        if response:
            return response
        else:
            return jsonify(msg="Error deleting class"), 500