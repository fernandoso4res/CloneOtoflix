from random import sample
from ext.auth import get_jwt_identity

def check_required_keys(data, keys):
    json_keys = get_all_json_keys(data)
    for key in keys:
        if key not in json_keys:
            raise KeyError("Missing required field: {}".format(key))
    return True

def check_allowed_keys(requested_keys, allowed_keys):
    data = {}
    for key in requested_keys:
        if key in allowed_keys:
            data[key] = requested_keys[key]
    return data

def get_all_json_keys(data, keys=None):
    keys = keys or []
    if isinstance(data, dict):
        keys += data.keys()
        _ = [get_all_json_keys(x, keys) for x in data.values()]
    elif isinstance(data, list):
        _ = [get_all_json_keys(x, keys) for x in data]
    return list(set(keys))


def check_allowed_fields(requested_fields, allowed_fields):
    return tuple(x for x in requested_fields if x in allowed_fields)


def generate_random_token(token_type, character_quantity):
    token = 'Token type not found'
    range_number = list(range(49, 58))
    range_letter_lower = list(range(97, 123))
    range_letter_upper = list(range(65, 91))

    match token_type:
        case 'numbers':
            token = ''.join(chr(i)
                            for i in sample(range_number, character_quantity))
        case 'letters_lower':
            token = ''.join(chr(i) for i in sample(
                range_letter_lower, character_quantity))
        case 'letters_upper':
            token = ''.join(chr(i) for i in sample(
                range_letter_upper, character_quantity))
        case 'letters_lower_and_upper':
            token = ''.join(chr(i) for i in sample(
                range_letter_lower + range_letter_upper, character_quantity))
        case 'letters_lower_and_numbers':
            token = ''.join(chr(i) for i in sample(
                range_letter_lower + range_number, character_quantity))
        case 'letters_upper_and_numbers':
            token = ''.join(chr(i) for i in sample(
                range_letter_upper + range_number, character_quantity))
        case 'letters_mixed_numbers':
            token = ''.join(chr(i) for i in sample(
                range_letter_lower + range_letter_upper + range_number, character_quantity))
        case _:
            token = 'Token type not found'
    return token

def check_allowed_file(filename, allowed_extensions):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

def get_logged_id():
    return get_jwt_identity()