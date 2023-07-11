
from LMS.db.es.es_support import fetch_records

from LMS.db.es import es_support


def get_sources(result):
    source_list = []
    for hit in result['hits']['hits']:
        source_list.append(hit['_source'])
    return source_list


def check_book_exists(book_id):
    query = {"query":
                 {"match":
                      {"book_id":book_id}
                  }
             }
    result = es_support.fetch_records('books', query)
    return 'hits' in result and result['hits']['total']['value'] > 0

