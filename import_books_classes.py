import json
from textbook_exchange.models import Textbook, Class

def mkflt(str_in):
    if str_in:
        return float(str_in)
    else:
        return 0

def mkint(str_in):
    if str_in:
        return int(str_in)
    else:
        return 0

# you can also keep this inside a view
with open("C:\\Users\\anlan\\Documents\\School Stuff\\2nd Year\\3240\\books_with_isbndb.json", encoding='utf-8') as data_file:
    json_data = json.loads(data_file.read())

    for book_data in json_data:
        try:
            book_obj = Textbook.objects.get(bookstore_isbn=book_data['ISBN'])
            setattr(book_obj, "isbn13", book_data['ISBN13'])
            setattr(book_obj, "isbn10", book_data['ISBN10'])
            setattr(book_obj, "title", book_data['Title'])
            setattr(book_obj, "author", book_data['Author'])
            setattr(book_obj, "req_type", book_data['Req Type'])
            setattr(book_obj, "cover_photo_url", book_data['Image Links'])
            setattr(book_obj, "bookstore_new_price", float(book_data['New'].replace('$', '').strip()))
            setattr(book_obj, "bookstore_used_price", float(book_data['Used'].replace('$', '').strip()))
            setattr(book_obj, "publisher", book_data['Publisher'])
            setattr(book_obj, "date", book_data['Publish Year'])
            setattr(book_obj, "description", book_data['Description'])
            setattr(book_obj, "page_count", mkint(book_data['Page Count']))
            setattr(book_obj, "google_rating", mkflt(book_data['Google Rating']))
            setattr(book_obj, "num_reviews", mkint(book_data['Number of Ratings']))
        except:
            book_obj = Textbook.create(**book_data)

        try:    
            class_obj = Class.objects.get(class_info=book_data['Dept']+book_data['Course']+"-"+book_data['Sect'])
            setattr(class_obj, "class_term", book_data['Term'])
            setattr(class_obj, "department", book_data['Dept'])
            setattr(class_obj, "course_code", book_data['Course'])
            setattr(class_obj, "section_number", book_data['Sect'])
            setattr(class_obj, "professor", book_data['Instructor'])
        except:
            class_obj = Class.create(**book_data)

        book_obj.class_objects.add(class_obj)