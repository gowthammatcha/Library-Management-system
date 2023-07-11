
from LMS.db.mongodb import mongo_support

#books=db['books']


def add_book(title,author,published_year,genre,isbn,count,availability):
    db = mongo_support.get_mongo_connection()
    books = db['books']
    book_id = books.count_documents({}) + 1
    book={
        "book_id":book_id,
        "title":title,
        "author":author,
        "published_year":published_year,
        "genre":genre,
        "isbn":isbn,
        "count":count,
        "availability":availability
    }
    result = mongo_support.insert_document('books',book)
    return result

# add_book("This is not your story","shavi sharma",2018,"NOVEL","2890-8243-2378",3,True)


#get book information by the id
def get_book_by_id(book_id):
    book = mongo_support.find_in_collection('books',{"book_id":book_id})
    return book
res1 = get_book_by_id(1)
print("Get book by id:",res1)

#get all books list or books with particular genre list
def get_books(genre=None):
    if genre:
        books_list = mongo_support.find_in_collection('books',{"genre":genre})
    else:
        books_list = mongo_support.find_in_collection('books',{})
    return books_list
# res2 = get_books("Adventure")
# print("Get book by Genre:",res2)
#
# res3 = get_books()
# print("list of all books:",res3)



#update book details by book id
def update_book(book_id,title=None,author=None,published_year=None,genre=None,isbn=None,count=None,availability=None):
    book = get_book_by_id(book_id)
    if not book:
        print(f"Error: Book with book_id {book_id} not found")
        return 0
    update_details = {}
    if not book_id:
        return 0
    if title:
        update_details["title"]=title
    if author:
        update_details["author"] = author
    if published_year:
        update_details["published_year"] = published_year
    if genre:
        update_details["genre"] = genre
    if isbn:
        update_details["isbn"] = isbn
    if count:
        update_details["count"] = count
    if availability:
        update_details["availability"] = availability
    result = mongo_support.update_document_by_query('books',{"book_id":book_id},update_details)
    return result


res4 = update_book(4,author="GERGOE-S-CLASON")
print("Book updated status:",res4)

#---->function to delete a book and user by id
def delete_book(book_id):
    result = mongo_support.delete_by_query('books',{"book_id":book_id})
    if hasattr(result, 'deleted_count') and result.deleted_count == 0:
        print(f"Error: Book with book_id: {book_id} is not found")
    else:
        print(f"Book with book_id: {book_id} is successfully deleted")
    return result.deleted_count if hasattr(result, 'deleted_count') else 0

#delete_book(6)




