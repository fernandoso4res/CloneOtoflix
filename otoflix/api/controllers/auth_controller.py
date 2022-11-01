import sys
import datetime
from flask import request, jsonify
from ext.auth import password_check, password_hash, create_access_token, set_access_cookies, get_jwt_identity, unset_jwt_cookies
from controllers.utils_controller import generate_random_token, check_required_keys, check_allowed_keys
from controllers.errors_controller import errors
from controllers.queue_controller import send_email
from repositories.mongodb_repository import check_if_exists, find_one, insert_one, update_one, delete_one
from repositories.redis_repository import check_if_key_exists, delete, set, get


def register_user(type):
    try:
        data = request.get_json()
        required_allowed_keys = ['first_name', 'last_name', 'email', 'nickname', 'password']
        check_required_keys(data, required_allowed_keys)
        data = check_allowed_keys(data, required_allowed_keys)
        if not check_if_exists('users', email=data['email']):
            data['password'] = password_hash(data['password'])
            data['user_type'] = type
            data['is_active'] = True
            data['registration_date'] = datetime.datetime.utcnow()
            data['general_ranking'] = 0
            data['simulated_ranking'] = 0
            id = insert_one('users', data)
            response = jsonify(msg="User registered successfully", id=id)
            if type == 'student':
                access_token = create_access_token(id, type)
                if update_one('users', {'jwt_token': access_token}, id=id):
                    set_access_cookies(response, access_token)
                    return response, 201
                else:
                    raise Exception("Error updating user")
            else:
                return response, 201
        else:
            return jsonify(msg="Email already registered"), 400
    except Exception as e:
        if check_if_exists('users', email=request.get_json()['email']):
            delete_one('users', email=request.get_json()['email'])
        response = errors(e)
        if response:
            return response
        else:
            return jsonify(msg="Error registering student"), 500


def login():
    try:
        print('login')
        data = request.get_json()
        required_keys = ['email', 'password']
        check_required_keys(data, required_keys)
        user = find_one('users', 'password', 'user_type',
                        'id', email=data['email'])
        if user:
            if password_check(data['password'], user['password']):
                response = jsonify(msg="Login successful")
                access_token = create_access_token(
                    user['id'], user['user_type'])
                update_one('users', {'jwt_token': access_token}, id=user['id'])
                set_access_cookies(response, access_token)
                print('vamos responder')
                return response, 201
            else:
                return jsonify(msg="Invalid email or password"), 401
        else:
            return jsonify(msg="Invalid email or password"), 401
    except Exception as e:
        response = errors(e)
        if response:
            return response
        else:
            return jsonify(msg="Error logging in"), 500

def logout():
    try:
        id = get_jwt_identity()
        response = jsonify(msg="Logout successful")
        unset_jwt_cookies(response)
        return response
    except Exception as e:
        print(e)
        response = errors(e)
        if response:
            return response
        else:
            return jsonify(msg="Error logging out"), 500

def teste():
    return jsonify(hello="world")

def change_password():
    try:
        data = request.get_json()
        required_keys = ['password', 'new_password']
        check_required_keys(data, required_keys)
        user = find_one('users', 'id', 'password', id=get_jwt_identity())
        if user:
            if password_check(data['password'], user['password']):
                update_one('users', {'password': password_hash(
                    data['new_password'])}, id=user['id'])
                return jsonify(msg="Password changed successfully"), 200
            return jsonify(msg="Invalid user or password"), 400
        return jsonify(msg="Invalid user or password"), 400
    except Exception as e:
        response = errors(e)
        if response:
            return response
        else:
            return jsonify(msg="Error changing password"), 500


def forgot_password_send_token():
    try:
        data = request.get_json()
        required_keys = ['email']
        check_required_keys(data, required_keys)
        user = find_one('users', 'id', 'first_name', 'email', email=data['email'])
        if user:
            valid_token = True
            while valid_token:
                # 6 é o numero de digitos que o token tera
                token = generate_random_token('numbers', 6)
                valid_token = check_if_key_exists(token)
            # 3600 é o Tempo de expiraçãod do token
            set(user['email'], token, 3600)
            send_email(user['email'], 'forgot_password_send_token', token=token, first_name=user['first_name'])
            return jsonify(msg="Token sent successfully"), 202
        else:
            return jsonify(msg="Invalid email"), 400
    except Exception as e:
        response = errors(e)
        if response:
            return response
        else:
            return jsonify(msg="Error sending token"), 500


def forgot_password_validate_token():
    try:
        data = request.get_json()
        required_keys = ['email', 'token']
        check_required_keys(data, required_keys)
        if check_if_key_exists(data['email']):
            if get(data['email']) == data['token']:
                return jsonify(msg="Token is valid"), 200
        return jsonify(msg="Invalid token"), 401
    except Exception as e:
        response = errors(e)
        if response:
            return response
        else:
            return jsonify(msg="Error validating token"), 500


def forgot_password_change_password():
    try:
        data = request.get_json()
        required_keys = ['email', 'token', 'new_password']
        check_required_keys(data, required_keys)
        if get(data['email']) == data['token']:
            if check_if_exists('users', email=data['email']):
                update_one('users', {'password': password_hash(data['new_password'])}, email=data['email'])
                delete(data['email'])
                return jsonify(msg="Password changed successfully"), 200
            return jsonify(msg="Invalid email or token"), 401
        return jsonify(msg="Invalid email or token"), 401
    except Exception as e:
        response = errors(e)
        if response:
            return response
        else:
            return jsonify(msg="Error changing password"), 500
