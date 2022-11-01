from cgi import print_arguments
import sys
from flask import request, jsonify
from controllers.utils_controller import check_allowed_fields, check_allowed_keys, check_required_keys
from controllers.errors_controller import errors
from repositories.mongodb_repository import check_if_exists, fields_of_query_param, filters_of_query_param, find_all, find_one, insert_one, replace_one, delete_one
from operator import itemgetter


def get_rankings():
    try:
        search_fields = ['id', 'first_name', 'last_name', 'nickname']
        fields = None
        ranking_type = None
        filters = {}
        if request.args.get('ranking_type'):
            if request.args.get('ranking_type') == 'general_ranking':
                search_fields.append('general_ranking')
                ranking_type = 'general_ranking'
            elif request.args.get('ranking_type') == 'simulated_ranking':
                search_fields.append('simulated_ranking')
                ranking_type = 'simulated_ranking'
            else:
                return jsonify(msg="Invalid ranking type"), 400
        else:
            return jsonify(msg="Invalid ranking type"), 400
        fields = tuple(search_fields)
        ranking = find_all('users', *fields, **filters)
        ranking.sort(key=itemgetter('simulated_ranking'), reverse=True)
        classification = 1
        for position in ranking:
            position['points'] = position.pop(ranking_type)
            position['position'] = classification
            classification += 1
        
        # criar função para calcular o desempenho do aluno
        for position in ranking:
            position['performance'] = ''
        return jsonify(ranking), 200
    except Exception as e:
        response = errors(e)
        if response:
            return response
        else:
            return jsonify(msg="Error searching ranking"), 500

def post_add_points():
    try:
        data = request.get_json()
        required_allowed_keys = ['ranking_name', 'point_amount']
        check_required_keys(data, required_allowed_keys)
        data = check_allowed_keys(data, required_allowed_keys)
        id = insert_one('students', data)
        return jsonify(msg="Flashcard successfully registered", id=id), 201
    except Exception as e:
        response = errors(e)
        if response:
            return response
        else:
            return jsonify(msg="Error creating flashcard"), 500


