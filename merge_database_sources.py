import json

with open('books_google_isbndb.json') as b:
    with open('uva_classes.json') as c:
            books = json.load(b)
            courses = json.load(c)['class_schedules']['records']
            for book in books:
                for course in courses:
                    if book['Dept'] == course[0] and book['Course'] == course[1]:
                        book['ClassTitle'] = course[4]
                        break
                if not 'ClassTitle' in book:
                    book['ClassTitle'] = book['Dept'] + "-" + book['Course']
    with open('class_data.json', 'w+') as f:
        json.dump(books, f, indent=4)