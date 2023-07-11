#from LMS.db.mongodb.mongo_support import db
#from LMS.db.mongodb.mongo_support import insert_document,get_document_by_id,find_in_collection,update_document_by_id, delete_by_id
from LMS.db.mongodb import mongo_support
# users = db['users']

def add_user(name,phone_no,email,book_id,book_name,issued_date,returned_date,returned_status):
    db = mongo_support.get_mongo_connection()
    users = db['users']
    user_id = users.count_documents({}) + 1
    user={
        "user_id":user_id,
        "name":name,
        "phone_no":phone_no,
        "email": email,
        "book_id":book_id,
        "book_name":book_name,
        "issue_date": issued_date,
        "returned_date":returned_date,
        "returned_status":returned_status
    }
    result = mongo_support.insert_document('users',user)
    return result

# res = add_user("Bhargav","9234783498","bhargav@test.com","6","The Richest man in the babylon","1 APRIL 2023","15 APRIL 2023", False)
# print("user added successfully:",res)

#------>
#*
#get user by id
def get_user_by_id(user_id):
    user = mongo_support.find_in_collection('users',{"user_id":user_id})
    return user
# res1 = get_user_by_id(1)
# print("Get User By id:",res1)

#Get all users
def get_users():
    user_list = mongo_support.find_in_collection('users',{})
    return user_list
# res2 = get_users()
# print("Users List:",res2)

#update the user by thier id
def update_user(user_id,name=None,phone_no=None,email=None,book_id=None,issue_date=None,returned_date=None,returned_status=None):
    user =  get_user_by_id(user_id)
    if not user:
        print(f"Error: user with user_id {user_id} not found")
        return 0
    update_details = {}
    if not user_id:
        return 0
    if name:
        update_details["name"] = name
    if phone_no:
        update_details["phone_no"] = phone_no
    if email:
        update_details["email"] = email
    if book_id:
        update_details["book_id"] = book_id
    if issue_date:
        update_details["issue_date"] = issue_date
    if returned_date:
        update_details["returned_date"] = returned_date
    if returned_status:
        update_details["returned_status"] = returned_status
    result = mongo_support.update_document_by_query('users',{"user_id":user_id},update_details)
    return result
    # return result.modified_count


# update_user(1,email="gowtham79@gmail.com")
# res4 = get_user_by_id(1)
# print("The user 1 details:",res4)

#delete the user by thier id
def delete_user(user_id):
    result = mongo_support.delete_by_query('users',{"user_id":user_id})
    if hasattr(result, 'deleted_count') and result.deleted_count == 0:
        print(f"Error: user with user_id: {user_id} is not found")
    else:
        print(f"Book with user_id: {user_id} is successfully deleted")
    return result.deleted_count if hasattr(result, 'deleted_count') else 0


delete_user(4)