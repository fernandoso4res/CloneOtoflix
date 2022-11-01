from flask import Blueprint
from flask_jwt_extended import jwt_required
from ext.auth import admin_required
from controllers import subscriptions_controller

bp = Blueprint('subscription', __name__)

@bp.route('/', methods=['POST'])
@jwt_required()
def post_subscriptions():
    return subscriptions_controller.post_subscriptions()

@bp.route('/', methods=['GET'])
@jwt_required()
def get_subscriptions():
    return subscriptions_controller.get_subscriptions()

@bp.route('/<id>', methods=['GET'])
@jwt_required()
def get_subscriptions_id(id):
    return subscriptions_controller.get_subscriptions_id(id)

@bp.route('/<id>', methods=['PUT'])
@jwt_required()
def put_subscriptions_id(id):
    return subscriptions_controller.put_subscriptions_id(id)

@bp.route('/<id>', methods=['DELETE'])
@jwt_required()
def delete_subscriptions_id(id):
    return subscriptions_controller.delete_subscriptions_id(id)
