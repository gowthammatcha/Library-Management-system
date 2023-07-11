import pymongo



def get_mongo_connection():
    client = pymongo.MongoClient("mongodb://localhost:27017")
    db = client['Library']
    return db

def insert_document(collection_name,document):
    db = get_mongo_connection()
    collection = db[collection_name]
    result = collection.insert_one(document)
    return result.inserted_id

def find_in_collection(collection_name,query):
    db = get_mongo_connection()
    collection = db[collection_name]
    result = collection.find(query)
    return list(result)

def update_document_by_query(collection_name,query,update_details):
    db = get_mongo_connection()
    collection = db[collection_name]
    result = collection.update_one(query,{"$set" : update_details})
    return result.modified_count



def delete_by_query(collection_name,query):
    db = get_mongo_connection()
    collection = db[collection_name]
    result = collection.delete_many(query)
    return result



# def get_document_by_id(collection_name,id_feild,id):
#     db = get_mongo_connection()
#     collection = db[collection_name]
#     result = collection.find_one({id_feild:id})
#     return result


# def update_document_by_id(collection_name,id_feild,book_id,update_details):
#     db = get_mongo_connection()
#     collection = db[collection_name]
#     result = collection.update_one({id_feild : book_id},{"$set" : update_details})
#     return result.modified_count


# def delete_by_id(collection_name,id_feild,id):
#     db = get_mongo_connection()
#     collection = db[collection_name]
#     result = collection.delete_one({id_feild: id})
#     return result


# def delete_all_docs(collection_name):
#     db = get_mongo_connection()
#     collection = db[collection_name]
#     result = collection.delete_many({})
#     return result.deleted_count




