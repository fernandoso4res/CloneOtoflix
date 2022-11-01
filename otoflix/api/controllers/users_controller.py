from flask import request, jsonify
from controllers.utils_controller import check_allowed_fields, check_required_keys, check_allowed_keys, check_allowed_file
from controllers.errors_controller import errors
from ext.auth import get_jwt_identity
from repositories.mongodb_repository import find_all, find_one, delete_one, check_if_exists, fields_of_query_param, delete_many, update_many, update_one, count
from repositories.storage_repository import upload_fileobj


def get_users():
    try:
        allowed_fields = ['id', 'first_name', 'last_name',
                          'email', 'registration_date', 'is_active', 'user_type']
        query_params = dict(request.args)
        fields = fields_of_query_param(query_params)
        if fields:
            fields = check_allowed_fields(fields, allowed_fields)
        else:
            fields = tuple(allowed_fields)
        filters = {}
        if request.args.get('user_type'):
            filters['user_type'] = request.args.get('user_type')
        return jsonify(find_all('users', *fields, **filters)), 200
    except Exception as e:
        response = errors(e)
        if response:
            return response
        else:
            return jsonify(msg="Error searching users"), 500

def get_users_id(id):
    try:
        allowed_fields = ['id', 'first_name', 'last_name',
                          'email', 'registration_date', 'is_active', 'user_type']
        query_params = dict(request.args)
        fields = fields_of_query_param(query_params)
        if fields:
            fields = check_allowed_fields(fields, allowed_fields)
        else:
            fields = tuple(allowed_fields)
        return jsonify(find_one('users', *fields, id=id)), 200
    except Exception as e:
        response = errors(e)
        if response:
            return response
        else:
            return jsonify(msg="Error searching user"), 500

def get_count():
    try:
        filters = {}
        if request.args.get('user_type'):
            filters['user_type'] = request.args.get('user_type')
        return jsonify(count=count('users', **filters)), 200
    except Exception as e:
        response = errors(e)
        if response:
            return response
        else:
            return jsonify(msg="Error counting user"), 500

def delete_users():
    try:
        data = request.args.to_dict(flat=False)
        if 'id' not in data or not isinstance(data['id'], list):
            raise KeyError
        ids = {}
        ids['id'] = data['id']
        ids['id'] = ','.join(ids['id'])
        delete_many('users', **ids)
        return '', 204
    except Exception as e:
        response = errors(e)
        if response:
            return response
        else:
            return jsonify(msg="Error deleting user"), 500

def delete_users_id(id):
    try:
        if not check_if_exists('users', id=id):
            return jsonify(msg='User not found'), 404
        delete_one('users', id=id)
        return '', 204
    except Exception as e:
        response = errors(e)
        if response:
            return response
        else:
            return jsonify(msg="Error deleting user"), 500

def patch_activate_deactivate():
    try:
        data = request.get_json()
        required_allowed_keys = ['ids', 'is_active']
        check_required_keys(data, required_allowed_keys)
        data = check_allowed_keys(data, required_allowed_keys)
        ids = {}
        ids['id'] = data['ids']
        ids['id'] = ','.join(ids['id'])
        del data['ids']
        if update_many('users', data, **ids):
            return jsonify(msg="Users successfully updated"), 200
        else:
            return jsonify(msg="Error updating users"), 500
    except Exception as e:
        response = errors(e)
        if response:
            return response
        else:
            return jsonify(msg="Error updating users"), 500

def patch_profile_picture():
    try:
        if 'file' not in request.files:
            raise KeyError
        data = request.files['file']
        allowed_extensions = ['jpg', 'jpeg', 'png']
        if not check_allowed_file(data.filename, allowed_extensions):
            return jsonify(msg="Invalid file extension"), 400
        id = get_jwt_identity()
        file_name = 'profile_picture/'+id+'.jpg'
        upload_fileobj('teste', file_name, data)
        return jsonify(msg="Profile picture successfully updated"), 201
    except Exception as e:
        response = errors(e)
        if response:
            return response
        else:
            return jsonify(msg="Error updating profile picture"), 500

def patch_profile_infos():
    try:
        data = request.get_json()
        required_allowed_keys = ['first_name', 'last_name', 'email', 'nickname']
        data = check_allowed_keys(data, required_allowed_keys)
        id = get_jwt_identity()
        if 'email' in data:
            user = find_one('users', 'email', id=get_jwt_identity())
            if data['email'] != user['email']:
                if check_if_exists('users', email=data['email']):
                    return jsonify(msg="Email already registered"), 400
        update_one('users', data, id=id)
        return jsonify(msg="Users successfully updated"), 200
    except Exception as e:
        response = errors(e)
        if response:
            return response
        else:
            return jsonify(msg="Error updating profile infos"), 500