import sys
from flask import request, jsonify
from controllers.utils_controller import check_required_keys
from controllers.errors_controller import errors
from repositories.mongodb_repository import find_all, find_one, insert_one, replace_one, delete_one, check_if_exists, fields_of_query_param, filters_of_query_param


def post_subscriptions():
    try:
        data = request.get_json()
        required_keys = ['subscription_name', 'subscription_description', 'subscription_price', 'subscription_duration_unit', 'subscription_duration_value', 'subscription_permissions', 'certificates',
                         'analysis', 'benefits_club', 'flashcards', 'simulations', 'questions_database', 'images_database', 'mentoring', 'monitoring', 'simulation_ranking', 'general_ranking', 'courses']
        check_required_keys(data, required_keys)
        if not isinstance(data['subscription_price'], float) or data['subscription_price'] <= 0:
            return jsonify(msg="Subscription price is invalid"), 400
        if data['subscription_duration_unit'] != 'dia(s)' and data['subscription_duration_unit'] != 'mes(es)' and data['subscription_duration_unit'] != 'ano(s)':
            return jsonify(msg="Subscription duration unit is invalid"), 400
        if not isinstance(data['subscription_duration_value'], int) or data['subscription_duration_value'] <= 0:
            return jsonify(msg="Subscription duration value is invalid"), 400
        id = insert_one('subscriptions', data)
        return jsonify(msg="Subscription successfully registered", id=id), 201
    except Exception as e:
        response = errors(e)
        if response:
            return response
        else:
            return jsonify(msg="Error creating subscription"), 500


def get_subscriptions():
    try:
        query_params = dict(request.args)
        fields = fields_of_query_param(query_params)
        filters = filters_of_query_param(query_params)
        return jsonify(find_all('subscriptions', *fields, **filters)), 200
    except Exception as e:
        response = errors(e)
        if response:
            return response
        else:
            return jsonify(msg="Error searching subscriptions"), 500


def get_subscriptions_id(id):
    try:
        query_params = dict(request.args)
        fields = fields_of_query_param(query_params)
        return jsonify(find_one('subscriptions', *fields, id=id)), 200
    except Exception as e:
        response = errors(e)
        if response:
            return response
        else:
            return jsonify(msg="Error searching subscription"), 500


def put_subscriptions_id(id):
    try:
        data = request.get_json()
        required_keys = ['subscription_name', 'subscription_description', 'subscription_price', 'subscription_duration_unit', 'subscription_duration_value', 'subscription_permissions', 'certificates',
                         'analysis', 'benefits_club', 'flashcards', 'simulations', 'questions_database', 'images_database', 'mentoring', 'monitoring', 'simulation_ranking', 'general_ranking', 'courses']
        check_required_keys(data, required_keys)
        if not check_if_exists('subscriptions', id=id):
            return jsonify(msn='Subscription not found'), 404
        if not isinstance(data['subscription_price'], float) or data['subscription_price'] <= 0:
            return jsonify(msg="Subscription price is invalid"), 400
        if data['subscription_duration_unit'] != 'dia(s)' and data['subscription_duration_unit'] != 'mes(es)' and data['subscription_duration_unit'] != 'ano(s)':
            return jsonify(msg="Subscription duration unit is invalid"), 400
        if not isinstance(data['subscription_duration_value'], int) or data['subscription_duration_value'] <= 0:
            return jsonify(msg="Subscription duration value is invalid"), 400
        replace_one('subscriptions', data, id=id)
        return jsonify(msg="Subscription successfully updated"), 200
    except Exception as e:
        response = errors(e)
        if response:
            return response
        else:
            return jsonify(msg="Error updating subscription"), 500


def delete_subscriptions_id(id):
    try:
        if not check_if_exists('subscriptions', id=id):
            return jsonify(msn='Subscription not found'), 404
        delete_one('subscriptions', id=id)
        return '', 204
    except Exception as e:
        response = errors(e)
        if response:
            return response
        else:
            return jsonify(msg="Error deleting subscription"), 500
