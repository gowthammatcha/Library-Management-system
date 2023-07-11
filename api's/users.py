import json
from LMS.db.es import es_support
from flask import Blueprint, Response,request as current_request , jsonify
from LMS.support.users_support import get_hits_source_list,check_user_exist
users_api = Blueprint('users_api', __name__)



#create Book Index
@users_api.route('/api/users/create_user', methods=['POST'])
def create_user_index():
    mappings = {
        "mappings": {
            "dynamic_templates": [
                {
                    "strings_as_keywords": {
                        "match_mapping_type":
                            "string",
                        "mapping": {
                            "type": "text",
                            "fields": {
                                "raw": {
                                    "type": "keyword"
                                }
                            }
                        }
                    }
                }
            ],
            "properties": {
                "timestamp": {
                    "type": "date"
                },
                "id": {
                    "type": "text"
                }
            }
        }
    }

    result = es_support.create_index('users',mappings)
    payload = current_request.get_json()
    return Response(response=json.dumps(result), status=200, content_type='application/json')

#add a user in LMS
@users_api.route('/api/users/create', methods=['POST'])
def create_user():
    payload = current_request.get_json()
    user = {
        'user_id': payload['user_id'],
        'name': payload['name'],
        'email': payload['email'],
        'books': payload['books']
    }
    result = es_support.insert_record('users',payload['user_id'],user)
    print(result)
    return jsonify(result)

#get the user details if the user_id is given otherwise all the get all other users
@users_api.route('/api/users/read/<string:user_id>',methods=['GET'])
@users_api.route('/api/users/read', methods=['GET'])
def read_user(user_id=None):
    if user_id:
        query = {"query":
                     {"match":
                          {"user_id":user_id}
                      }
                 }
    else:
        query = {"query":{"match_all":{}}}
    source_list = get_hits_source_list('users', query)
    return Response(response=json.dumps(source_list), status=200, content_type='application/json')
    #return jsonify(result)



@users_api.route('/api/users/update/<string:user_id>', methods=['POST'])
def update_user(user_id):
    payload = current_request.get_json()
    # checking if user ID exists in our records
    if not check_user_exist(user_id):
        # user ID not found in database
        error_message = f"user with ID '{user_id}' not found"
        return Response(response=json.dumps({'error': error_message}), status=404, content_type='application/json')
    # update user details
    result = es_support.insert_record('users', user_id, payload)
    return Response(response=json.dumps(result), status=200, content_type='application/json')


#delete the user details the user id

@users_api.route('/api/users/delete/<string:user_id>', methods=['DELETE'])
def delete_user(user_id):
    #payload = current_request.get_json()
    result = es_support.delete_record('users', user_id )
    return Response(response=json.dumps(result), status=200, content_type='application/json')

