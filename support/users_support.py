from LMS.db.es import es_support

def get_hits_source_list(index, query):
    result = es_support.fetch_records(index, query)
    source_list = []
    for hit in result['hits']['hits']:
        source_list.append(hit['_source'])
    return source_list


def check_user_exist(user_id):
    query = {"query": {"match": {"user_id": user_id}}}
    result = es_support.fetch_records('users', query)
    return result['hits']['hits']


