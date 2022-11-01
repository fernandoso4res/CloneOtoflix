from datetime import datetime, timedelta, timezone
from functools import wraps
from flask_jwt_extended import JWTManager, verify_jwt_in_request, get_jwt
from flask_jwt_extended import utils as jwt_functions
from flask import jsonify
from config import JWT_REFRESH_EXPIRES
import bcrypt

jwt = JWTManager()


def init_app(app):
    jwt.init_app(app)

    @app.after_request
    def refresh_expiring_jwts(response):
        try:
            exp_timestamp = get_jwt()["exp"]            
            now = datetime.now(timezone.utc)
            target_timestamp = datetime.timestamp(now + JWT_REFRESH_EXPIRES)
            if target_timestamp > exp_timestamp:
                access_token = create_access_token(identity=get_jwt_identity())
                set_access_cookies(response, access_token)
            return response
        except (RuntimeError, KeyError):
            # Case where there is not a valid JWT. Just return the original response
            return response


# Funções relacionadas ao flask_jwt_extended

def create_access_token(user_id, user_type):
    return jwt_functions.create_access_token(identity=user_id, additional_claims={'user_type': user_type})

def set_access_cookies(response, access_token):
    jwt_functions.set_access_cookies(response, access_token)

def unset_jwt_cookies(response):
    jwt_functions.unset_jwt_cookies(response)

def get_jwt_identity():
    return jwt_functions.get_jwt_identity()

def admin_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims['user_type'] == 'administrator':
                return fn(*args, **kwargs)
            else:
                return jsonify(msg="Admins only!"), 403
        return decorator
    return wrapper


def teacher_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims['user_type'] == 'teacher':
                return fn(*args, **kwargs)
            else:
                return jsonify(msg="Admins only!"), 403
        return decorator
    return wrapper


def admin_or_teacher_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims['user_type'] == 'administrator' or claims['user_type'] == 'teacher':
                return fn(*args, **kwargs)
            else:
                return jsonify(msg="Admins only!"), 403
        return decorator
    return wrapper


# Funções relacionadas ao bcrypt

def password_hash(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def password_check(password, hash):
    return bcrypt.checkpw(password.encode('utf-8'), hash.encode('utf-8'))
