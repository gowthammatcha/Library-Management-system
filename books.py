import json
from LMS.db.es import es_support
from flask import Blueprint, Response,request as current_request , jsonify
from LMS.support.books_support import get_sources,check_book_exists

books_api = Blueprint('books_api', __name__)

#create Book Index
@books_api.route('/api/books/create_index', methods=['POST'])
def create_book_index():
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
    result = es_support.create_index('books',mappings)
    payload = current_request.get_json()
    return Response(response=json.dumps(result), status=200, content_type='application/json')

#add a book in the LMS
@books_api.route('/api/books/create', methods=['POST'])
def create_book():
    payload = current_request.get_json()
    book = {
        'book_id': payload['book_id'],
        'title': payload['title'],
        'author': payload['author'],
        'publisher': payload['publisher'],
        'isbn': payload['isbn'],
        'genre': payload['genre'],
        'count': payload['count'],
        'availability': payload['availability']
    }
    result = es_support.insert_record('books',payload['book_id'],book)
    print(result)
    return Response(response=json.dumps(result), status=200, content_type='application/json')
    #return jsonify(result)



#get the book if the id is given otherwise all the books
@books_api.route('/api/books/read/<string:book_id>',methods=['GET'])
@books_api.route('/api/books/read', methods=['GET'])
def read_book(book_id=None):
    if book_id:
        query = {"query":
                     {"match":
                          {"book_id":book_id}
                      }
                 }
    else:
        query = {"query":{"match_all":{}}}
    result = es_support.fetch_records('books',query)
    source_list = get_sources(result)
    return Response(response=json.dumps(source_list), status=200, content_type='application/json')




#----->Update the Book by id
@books_api.route('/api/books/update/<string:book_id>', methods=['POST'])
def update_book(book_id):
    payload = current_request.get_json()
    # checking if book-id exists in our records
    if not check_book_exists(book_id):
        # book-id not found
        error_message = f"Book with ID '{book_id}' not found"
        return Response(response=json.dumps({'error': error_message}), status=404, content_type='application/json')
    # update book details
    result = es_support.insert_record('books',book_id,payload)
    return Response(response=json.dumps(result), status=200, content_type='application/json')


#--->delete the book_by id
@books_api.route('/api/books/delete/<string:book_id>', methods=['DELETE'])
def delete_book(book_id):
    #payload = current_request.get_json()
    result = es_support.delete_record('books', book_id)
    return Response(response=json.dumps(result), status=200, content_type='application/json')



