from flask import request, jsonify
from controllers.utils_controller import check_allowed_keys, check_required_keys, get_logged_id
from controllers.errors_controller import errors
from repositories.mongodb_repository import check_if_exists, update_one_incrementally

def post_add_points():
    try:
        data = request.get_json()
        required_allowed_keys = ['points', 'ranking_type']
        check_required_keys(data, required_allowed_keys)
        data = check_allowed_keys(data, required_allowed_keys)
        id = get_logged_id()
        if data['ranking_type'] == 'general_ranking':
            data['general_ranking'] = data.pop('points')
            del data['ranking_type']
        elif data['ranking_type'] == '':
            data['simulated_ranking'] = data.pop('points')
            del data['ranking_type']
        else:
            return jsonify(msg="Invalid ranking type"), 400
        update_one_incrementally('users', data, id=id)
        return jsonify(msg="User points successfully updated"), 201
    except Exception as e:
        response = errors(e)
        if response:
            return response
        else:
            return jsonify(msg="Error updating user points"), 500

def post_add_points_by_id():
    try:
        data = request.get_json()
        required_allowed_keys = ['id', 'points', 'ranking_type']
        check_required_keys(data, required_allowed_keys)
        data = check_allowed_keys(data, required_allowed_keys)
        id = data.pop('id')
        if data['ranking_type'] == 'general_ranking':
            data['general_ranking'] = data.pop('points')
            del data['ranking_type']
        elif data['ranking_type'] == 'simulated_ranking':
            data['simulated_ranking'] = data.pop('points')
            del data['ranking_type']
        else:
            return jsonify(msg="Invalid rank type"), 400
        update_one_incrementally('users', data, id=id)
        return jsonify(msg="User points successfully updated"), 201
    except Exception as e:
        response = errors(e)
        if response:
            return response
        else:
            return jsonify(msg="Error updating user points"), 500


