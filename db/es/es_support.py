from elasticsearch import Elasticsearch

def get_es_connection():
    es = Elasticsearch('https://0.0.0.0:9200', http_auth=('mgowtham1', 'gowtham123'),verify_certs=False)
    # es = Elasticsearch('https://0.0.0.0:9200')
    return es



def create_index(index_name,mappings):
    es = get_es_connection()
    result = es.indices.create(index=index_name, body=mappings)
    return result

def insert_record(table_name,id,data):
    es = get_es_connection()
    result = es.index(index= table_name , id=id ,body = data)
    return result

def fetch_records(table_name,query):
    es = get_es_connection()
    result = es.search(index= table_name, body=query)
    return result

# def update_record(table_name,record_id,update_query):
#     es = get_es_connection()
#     result = es.update(index=table_name,id=record_id,body=update_query)
#     return result

def delete_record(table_name,record_id):
    es = get_es_connection()
    result = es.delete(index=table_name,id=record_id)
    return result

