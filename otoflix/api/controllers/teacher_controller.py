import sys
from flask import request, jsonify
from controllers.utils_controller import check_allowed_keys, check_required_keys
from controllers.errors_controller import errors
from controllers.queue_controller import send_to_queue
from repositories.mongodb_repository import check_if_exists, fields_of_query_param, filters_of_query_param, find_all, find_one, insert_one, replace_one, delete_one

def post_teacher():
    try:
        data = request.get_json()
        required_allowed_keys = ['class', 'title', 'description', 'image']
        check_required_keys(data, required_allowed_keys)
        data = check_allowed_keys(data, required_allowed_keys)
        id = insert_one('teacher', data)
        return jsonify(msg="Class succesfully registered", id=id), 201
    except Exception as e:
        response = errors(e)
        if response:
            return response
        else: 
            return jsonify(msg="Error creating class"), 500