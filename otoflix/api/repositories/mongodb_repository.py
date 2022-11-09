from os import PRIO_USER
from bson import ObjectId

from ext.database import users_db, courses_db, questions_db, benefits_club_bd


def get_collection(collection):
    match collection:
        case 'classes':
            return classes_db.db.classes
        case 'modules':
            return courses_db.db.modules
        case 'users':
            return users_db.db.users
        case 'subscriptions':
            return users_db.db.subscriptions
        case 'courses':
            return courses_db.db.courses
        case 'questions':
            return questions_db.db.questions
        case 'flashcards':
            return questions_db.db.flashcards
        case 'simulated':
            return questions_db.db.simulated
        case 'decks':
            return questions_db.db.decks
        case 'benefits_club':
            return benefits_club_bd.db.benefits_club
        
        


# Funções que realizam consultas no banco 

def check_if_exists(collection, **filter):
    collection = get_collection(collection)
    document = collection.find_one(normalize_filters(filter))
    if document:
        return True
    else:
        return False

def find_all(collection, *fields: str, **filter):
    collection = get_collection(collection)
    results = collection.find(normalize_filters(filter), fields_to_projection(fields))
    result_aux = []
    for result in results:
        if '_id' in result:
            result['_id'] = str(result['_id'])
            result['id'] = result.pop('_id')
        result_aux.append(result)
    return result_aux

def find_one(collection, *fields: str, **filter):
    collection = get_collection(collection)
    result = collection.find_one(normalize_filters(filter), fields_to_projection(fields))
    if not result: result = {}
    if '_id' in result:
        result['_id'] = str(result['_id'])
        result['id'] = result.pop('_id')
    return result

def insert_many(collection, data):
    collection = get_collection(collection)
    collection = insert_many(data)
    return str(data['_id'])

def insert_one(collection, data):
    collection = get_collection(collection)
    collection.insert_one(data)    
    return str(data['_id'])

def update_one(collection, data, **filter):
    collection = get_collection(collection)
    result = collection.update_one(normalize_filters(filter), {'$set': data})
    return True if result.matched_count > 0 else False

def update_one_incrementally(collection, data, **filter):
    collection = get_collection(collection)
    result = collection.update_one(normalize_filters(filter), {'$inc': data})
    return True if result.matched_count > 0 else False

def update_many(collection, data, **filter):
    collection = get_collection(collection)
    result = collection.update_many(normalize_filters(filter), {'$set': data})
    return True if result.matched_count > 0 else False


def replace_one(collection, data, **filter):
    collection = get_collection(collection)
    result = collection.replace_one(normalize_filters(filter), data)
    return True if result.matched_count > 0 else False

def delete_one(collection, **filter):
    collection = get_collection(collection)
    collection.delete_one(normalize_filters(filter))

def delete_many(collection, **filter):
    collection = get_collection(collection)
    collection.delete_many(normalize_filters(filter))

def count(collection, **filter):
    collection = get_collection(collection)
    return collection.count_documents(normalize_filters(filter))


# Funções de normalização / formatação de dados

def fields_to_projection(fields):
    projection = {}
    if fields:
        for field in fields:
            if isinstance(field, dict):
                if '$elemMatch' in field:
                    projection[list(field['$elemMatch'])[0]] = field['$elemMatch'][list(field['$elemMatch'])[0]]
                continue
            if field == 'id':
                projection['_id'] = 1
                continue
            projection[field] = 1
        if not '_id' in projection:
            projection['_id'] = 0
    return projection

def format_filter(filter):
    if 'id' in filter:
        filter['_id'] = filter.pop('id')
        filter['_id'] = ObjectId(filter['_id'])
    return filter

def fields_of_query_param(query_params):
    if 'fields' not in query_params:
        return ''    
    fields = query_params['fields']
    fields = tuple(map(str, fields.split(',')))    
    fields = tuple("".join(x.split()) for x in fields)    
    fields = tuple(x for x in fields if x != '')
    return fields

def filters_of_query_param(query_params):
    filter = {}
    for key in list(query_params):
        if key.startswith('filter[') and key.endswith(']'):
            filter[key] = query_params[key]
    return filter

def normalize_filters(filter):
    for key in list(filter):
        filter[key] = filter[key].replace('true', 'True')
        filter[key] = filter[key].replace('false', 'False')
        filter[key] = eval_list(filter[key])
        filter[key] = {'$in' : filter[key]}
        if key.startswith('filter[') and key.endswith(']'):
            filter[key[7:-1]] = filter.pop(key)
    if 'id' in filter:
        filter['_id'] = filter.pop('id')
        filter['_id']['$in'] = [ObjectId(x) for x in filter['_id']['$in']]
    return filter

def normalize_id(id):
    return ObjectId(id) if ObjectId.is_valid(id) else id

def eval_list(s):
    try:
        s = eval(s)
        if isinstance(s, tuple):
            return list(s)
        else:
            return [s]    
    except:
        s = s.split(",")
        return [x.strip() for x in s]