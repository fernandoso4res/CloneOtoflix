import sys                 
from flask import request, jsonify
from controllers.utils_controller import check_allowed_keys, check_required_keys
from controllers.errors_controller import errors
from controllers.queue_controller import send_to_queue
from repositories.mongodb_repository import check_if_exists, fields_of_query_param, filters_of_query_param, find_all, find_one, insert_one, replace_one, delete_one
                     
def post_modules():
    try:         
        data = request.get_json()
        required_allowed_keys = ['Modulos:{"nome", "liberar_apos"}']
        check_required_keys(data, required_allowed_keys)
        data = check_allowed_keys(data, required_allowed_keys)
        id = insert_one('Modulos', data)
        return jsonify(msg="Module succesfully registered", id=id), 201
    except Exception as e:
        response = errors(e)
        if response:
            return response
        else:  
            return jsonify(msg="Error creating module"), 500


def get_modules():
    try:
        query_params = dict(request.args)
        fields = fields_of_query_param(query_params)
        filters = filters_of_query_param(query_params)
        return jsonify(find_all('modules', *fields, **filters)), 200
    except Exception as e:
        response = errors(e)
        if response:
            return response
        else:
            return jsonify(msg="Error searching modules"), 500