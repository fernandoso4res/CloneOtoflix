import sys
from flask import request, jsonify
from controllers.utils_controller import check_allowed_keys, check_required_keys
from controllers.errors_controller import errors
from repositories.mongodb_repository import check_if_exists, fields_of_query_param, filters_of_query_param, find_all, find_one, insert_one, replace_one, delete_one


def post_decks():
    try:
        data = request.get_json()
        required_allowed_keys = ['title', 'flashcards']
        check_required_keys(data, required_allowed_keys)
        data = check_allowed_keys(data, required_allowed_keys)
        categories = []
        for  flashcard in data['flashcards']:
            category = find_one('flashcards', 'category', id=flashcard['id'])
            if not category:
                raise KeyError ('Flashcard Id')
            categories.append(category['category'])
        categories = sorted(set(categories))
        data['categories'] = categories
        id = insert_one('decks', data)
        return jsonify(msg="Deck successfully registered", id=id), 201
    except Exception as e:
        response = errors(e)
        if response:
            return response
        else:
            return jsonify(msg="Error creating deck"), 500


def get_decks():
    try:
        query_params = dict(request.args)
        fields = fields_of_query_param(query_params)
        filters = filters_of_query_param(query_params)
        return jsonify(find_all('decks', *fields, **filters)), 200
    except Exception as e:
        response = errors(e)
        if response:
            return response
        else:
            return jsonify(msg="Error searching decks"), 500


def get_decks_id(id):
    try:
        query_params = dict(request.args)
        fields = fields_of_query_param(query_params)
        return jsonify(find_one('decks', *fields, id=id)), 200
    except Exception as e:
        response = errors(e)
        if response:
            return response
        else:
            return jsonify(msg="Error searching deck"), 500


def put_decks_id(id):
    try:
        data = request.get_json()
        required_allowed_keys = ['title', 'flashcards']
        check_required_keys(data, required_allowed_keys)
        data = check_allowed_keys(data, required_allowed_keys)
        if not check_if_exists('decks', id=id):
            return jsonify(msn='Deck not found'), 404
        categories = []
        for  flashcard in data['flashcards']:
            category = find_one('flashcards', 'category', id=flashcard['id'])
            if not category:
                raise KeyError ('Flashcard Id')
            categories.append(category['category'])
        categories = sorted(set(categories))
        data['categories'] = categories
        replace_one('decks', data, id=id)
        return jsonify(msg="Deck successfully updated"), 200
    except Exception as e:
        response = errors(e)
        if response:
            return response
        else:
            return jsonify(msg="Error updating deck"), 500


def delete_decks_id(id):
    try:
        if not check_if_exists('decks', id=id):
            return jsonify(msn='deck not found'), 404
        delete_one('decks', id=id)
        return '', 204
    except Exception as e:
        response = errors(e)
        if response:
            return response
        else:
            return jsonify(msg="Error deleting deck"), 500
