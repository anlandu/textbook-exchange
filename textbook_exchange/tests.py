from django.test import TestCase
from django.test import Client
from textbook_exchange.models import User, Class, Textbook, ProductListing
from django.utils import timezone
from django.core.exceptions import ValidationError
from textbook_exchange.forms import *
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files.uploadedfile import UploadedFile
from django.core.files import File
from django.urls import *
from . import *
from django.test import Client, override_settings
from unittest.mock import MagicMock, Mock

class SetUp(TestCase):
    def setUp(self):
        self.test_user = Users.objects.create(
            username = "", 
            password="", 
            first_name="", 
            last_name="", 
            email="",
            is_staff=False,
            date_joined = timezone.now()
        )

class AutocompleteTest(TestCase):

    '''
    Since we don't have all the books and courses in yet I don't know what
    the results will be but this is the format for the autocomplete tests
    '''

    fixtures = ['testing_data/textbooks.json', 'testing_data/classes.json']

    def test_template(self):
        search = "test_search" #this should return no results
        expected_results = {'search': 'test_search', 'books': [], 'courses': []}

        response = self.client.get('/buy/autocomplete/', {'search': search})

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            expected_results
        )

    def test_title_1(self):
        search = "and"
        expected_results = {'search': 'and', 'books': ['{\n    "_state": {\n        "adding": false,\n        "db": "default"\n    },\n    "author": "[\'Sandra J. Peterson\', \'Timothy S. Bredow\']",\n    "bookstore_isbn": "0-06-000044-9",\n    "bookstore_new_price": 73.99,\n    "bookstore_used_price": 55.22,\n    "cover_photo": "",\n    "cover_photo_url": "{\'smallThumbnail\': \'http://books.google.com/books/content?id=dPWtHAAACAAJ&printsec=frontcover&img=1&zoom=5&source=gbs_api\', \'thumbnail\': \'http://books.google.com/books/content?id=dPWtHAAACAAJ&printsec=frontcover&img=1&zoom=1&source=gbs_api\'}",\n    "date": "2016-01-29",\n    "description": "A complete and detailed book focused on middle range theories. The text examines theories and their applications in clinical nursing research and practice. In this fourth edition, the change of the subtitle to \\"Application to Nursing Research \\"and \\"Practice\\" better reflects the dynamic relationship between theory, research, and practice with an increased emphasis on applications of middle range theories to practice. The authors provide expert advice on selecting the appropriate theory for a nursing research project and developing the critical thinking skills needed to critique theories. Every theory chapter includes examples of the theories and ways they are used in research, as well as sample applications, and critical thinking exercises. Students can go to thePoint to find a related Theory Analysis exercise and practice their critiquing skills by doing the exercise and then comparing it with a crtique done by an expert in the field.",\n    "google_rating": 0.0,\n    "isbn10": "0060000449",\n    "isbn13": "9780060000448",\n    "num_reviews": 0,\n    "page_count": 344,\n    "publisher": "LWW",\n    "req_type": "Required",\n    "title": "Middle Range Theories: Application to Nursing Research and Practice"\n}', '{\n    "_state": {\n        "adding": false,\n        "db": "default"\n    },\n    "author": "[\'Martin Luther King\']",\n    "bookstore_isbn": "0-06-064691-8",\n    "bookstore_new_price": 29.99,\n    "bookstore_used_price": 14.91,\n    "cover_photo": "",\n    "cover_photo_url": "{\'smallThumbnail\': \'http://books.google.com/books/content?id=mTb_yAEACAAJ&printsec=frontcover&img=1&zoom=5&source=gbs_api\', \'thumbnail\': \'http://books.google.com/books/content?id=mTb_yAEACAAJ&printsec=frontcover&img=1&zoom=1&source=gbs_api\'}",\n    "date": "1990-12-07",\n    "description": "\\"We\'ve got some difficult days ahead,\\" civil rights activist Martin Luther King, Jr., told a crowd gathered at Memphis\'s Clayborn Temple on April 3, 1968. \\"But it really doesn\'t matter to me now because I\'ve been to the mountaintop. . . . And I\'ve seen the promised land. I may not get there with you. But I want you to know tonight that we as a people will get to the promised land.\\" These prohetic words, uttered the day before his assassination, challenged those he left behind to see that his \\"promised land\\" of racial equality became a reality; a reality to which King devoted the last twelve years of his life. These words and other are commemorated here in the only major one-volume collection of this seminal twentieth-century American prophet\'s writings, speeches, interviews, and autobiographical reflections. A Testament of Hope contains Martin Luther King, Jr.\'s essential thoughts on nonviolence, social policy, integration, black nationalism, the ethics of love and hope, and more.",\n    "google_rating": 4.0,\n    "isbn10": "0060646918",\n    "isbn13": "9780060646912",\n    "num_reviews": 3,\n    "page_count": 736,\n    "publisher": "Harper Collins",\n    "req_type": "Required",\n    "title": "A Testament of Hope: The Essential Writings and Speeches of Martin Luther King, Jr."\n}', '{\n    "_state": {\n        "adding": false,\n        "db": "default"\n    },\n    "author": "[\'Saff, Donald , 1937-\']",\n    "bookstore_isbn": "0-03-085663-9",\n    "bookstore_new_price": 209.95,\n    "bookstore_used_price": 40.0,\n    "cover_photo": "",\n    "cover_photo_url": "https://images.isbndb.com/covers/66/31/9780030856631.jpg",\n    "date": "1978",\n    "description": "Text And More Than 700 Illustrations Explain The Procedures And Techniques Of Five Kinds Of Printmaking: Lithography, Relief Printing, Intaglio, Seriography, And Combined Methods. Preface -- Introduction -- Pt. 1. Relief -- Ch. 1. History Of Relief -- Ch. 2. Relief Techniques -- Basic Woodcut Techniques -- The Classic Japanese Woodcut Technique (ukiyo-e) -- Wood Engraving -- Other Approaches To The Relief Print -- Pt. 2. Intaglio -- Ch. 3. History Of Intaglio -- Ch. 4. Intaglio Techniques -- Intaglio Print Characteristics -- Photographic Techniques And Collagraph Processes -- Pt. 3. Lithography -- Ch. 5. History Of Lithography -- Lithography Techniques -- Materials And Basic Chemistry -- Preparing The Stone Or Metal Plate -- Inks And Papers -- Printing -- Special Lithographic Techniques -- Photolithography. Pt. 4. Serigraphy -- Ch. 7. History Of Serigraphy -- Ch. 8. Serigraphy Techniques -- Materials And Equipment -- Stencil Making Techniques -- Photographic Techniques -- Printing -- Pt. 5. Trends : Processes/surfaces -- Ch. 9. Expanded And Applied Techniques -- Ch. 10. Papers, Papermaking, Curating Of Prints -- Papers And Papermaking -- The Curating Of Prints -- Appendix A : The Chemistry Of Etching -- Appendix B : Steel Facing -- Appendix C : Presses -- List Of Suppliers -- Bibliography -- Glossary -- Index -- Photographic Sources. Donald Saff, Deli Sacilotto. Includes Index. Bibliography: P. 422-424.",\n    "google_rating": 0.0,\n    "isbn10": "0030856639",\n    "isbn13": "9780030856631",\n    "num_reviews": 0,\n    "page_count": 436,\n    "publisher": "Holt, Rinehart And Winston",\n    "req_type": "Recommended",\n    "title": "Printmaking: History And Process"\n}'], 'courses': ['{\n    "_state": {\n        "adding": false,\n        "db": "default"\n    },\n    "class_info": "AAS3200-1",\n    "class_term": "2020EUVA",\n    "class_title": "Martin, Malcolm and America",\n    "course_code": "3200",\n    "department": "AAS",\n    "professor": "HADLEY",\n    "section_number": "1"\n}']}

        response = self.client.get('/buy/autocomplete/', {'search': search})

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            expected_results
        )

    def test_number_1(self):
        search = "12"

        expected_results = {'search': '12', 'books': ['{\n    "_state": {\n        "adding": false,\n        "db": "default"\n    },\n    "author": "[\'Thornton Wilder\']",\n    "bookstore_isbn": "0-06-051263-6",\n    "bookstore_new_price": 14.99,\n    "bookstore_used_price": 7.45,\n    "cover_photo": "",\n    "cover_photo_url": "{\'smallThumbnail\': \'http://books.google.com/books/content?id=8NmKkgrmj5EC&printsec=frontcover&img=1&zoom=5&edge=curl&source=gbs_api\', \'thumbnail\': \'http://books.google.com/books/content?id=8NmKkgrmj5EC&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api\'}",\n    "date": "2003-09-23",\n    "description": "Our Town was first produced and published in 1938 to wide acclaim. This Pulitzer Prize\\u2013winning drama of life in the town of Grover \'s Corners, an allegorical representation of all life, has become a classic. It is Thornton Wilder\'s most renowned and most frequently performed play. It is now reissued in this handsome hardcover edition, featuring a new Foreword by Donald Margulies, who writes, \\"You are holding in your hands a great American play. Possibly the great American play.\\" In addition, Tappan Wilder has written an eye-opening new Afterword, which includes Thornton Wilder\'s unpublished notes and other illuminating photographs and documentary material.",\n    "google_rating": 4.5,\n    "isbn10": "0060512636",\n    "isbn13": "9780060512637",\n    "num_reviews": 2,\n    "page_count": 208,\n    "publisher": "Harper Collins",\n    "req_type": "Required",\n    "title": "Our Town: A Play in Three Acts"\n}', '{\n    "_state": {\n        "adding": false,\n        "db": "default"\n    },\n    "author": "[\'Martin Luther King\']",\n    "bookstore_isbn": "0-06-064691-8",\n    "bookstore_new_price": 29.99,\n    "bookstore_used_price": 14.91,\n    "cover_photo": "",\n    "cover_photo_url": "{\'smallThumbnail\': \'http://books.google.com/books/content?id=mTb_yAEACAAJ&printsec=frontcover&img=1&zoom=5&source=gbs_api\', \'thumbnail\': \'http://books.google.com/books/content?id=mTb_yAEACAAJ&printsec=frontcover&img=1&zoom=1&source=gbs_api\'}",\n    "date": "1990-12-07",\n    "description": "\\"We\'ve got some difficult days ahead,\\" civil rights activist Martin Luther King, Jr., told a crowd gathered at Memphis\'s Clayborn Temple on April 3, 1968. \\"But it really doesn\'t matter to me now because I\'ve been to the mountaintop. . . . And I\'ve seen the promised land. I may not get there with you. But I want you to know tonight that we as a people will get to the promised land.\\" These prohetic words, uttered the day before his assassination, challenged those he left behind to see that his \\"promised land\\" of racial equality became a reality; a reality to which King devoted the last twelve years of his life. These words and other are commemorated here in the only major one-volume collection of this seminal twentieth-century American prophet\'s writings, speeches, interviews, and autobiographical reflections. A Testament of Hope contains Martin Luther King, Jr.\'s essential thoughts on nonviolence, social policy, integration, black nationalism, the ethics of love and hope, and more.",\n    "google_rating": 4.0,\n    "isbn10": "0060646918",\n    "isbn13": "9780060646912",\n    "num_reviews": 3,\n    "page_count": 736,\n    "publisher": "Harper Collins",\n    "req_type": "Required",\n    "title": "A Testament of Hope: The Essential Writings and Speeches of Martin Luther King, Jr."\n}'], 'courses': ['{\n    "_state": {\n        "adding": false,\n        "db": "default"\n    },\n    "class_info": "AAS3500-12",\n    "class_term": "2020EUVA",\n    "class_title": "Intermediate Seminar in AAS",\n    "course_code": "3500",\n    "department": "AAS",\n    "professor": "SMITHSON",\n    "section_number": "12"\n}']}

        response = self.client.get('/buy/autocomplete/', {'search': search})
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, expected_results)

    
    def test_no_results(self):
        search = "asdfghjkl"

        #limited to 6 of each
        expected_results = {
            "search": "asdfghjkl",
            "books": [],
            "courses": []
        }

        response = self.client.get('/buy/autocomplete/', {'search': search})

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            expected_results
        )

    def test_isbn_1(self):
        search = "9780060646912"

        #just expecting the single correct book
        expected_results = {'search': '9780060646912', 'books': ['{\n    "_state": {\n        "adding": false,\n        "db": "default"\n    },\n    "author": "[\'Martin Luther King\']",\n    "bookstore_isbn": "0-06-064691-8",\n    "bookstore_new_price": 29.99,\n    "bookstore_used_price": 14.91,\n    "cover_photo": "",\n    "cover_photo_url": "{\'smallThumbnail\': \'http://books.google.com/books/content?id=mTb_yAEACAAJ&printsec=frontcover&img=1&zoom=5&source=gbs_api\', \'thumbnail\': \'http://books.google.com/books/content?id=mTb_yAEACAAJ&printsec=frontcover&img=1&zoom=1&source=gbs_api\'}",\n    "date": "1990-12-07",\n    "description": "\\"We\'ve got some difficult days ahead,\\" civil rights activist Martin Luther King, Jr., told a crowd gathered at Memphis\'s Clayborn Temple on April 3, 1968. \\"But it really doesn\'t matter to me now because I\'ve been to the mountaintop. . . . And I\'ve seen the promised land. I may not get there with you. But I want you to know tonight that we as a people will get to the promised land.\\" These prohetic words, uttered the day before his assassination, challenged those he left behind to see that his \\"promised land\\" of racial equality became a reality; a reality to which King devoted the last twelve years of his life. These words and other are commemorated here in the only major one-volume collection of this seminal twentieth-century American prophet\'s writings, speeches, interviews, and autobiographical reflections. A Testament of Hope contains Martin Luther King, Jr.\'s essential thoughts on nonviolence, social policy, integration, black nationalism, the ethics of love and hope, and more.",\n    "google_rating": 4.0,\n    "isbn10": "0060646918",\n    "isbn13": "9780060646912",\n    "num_reviews": 3,\n    "page_count": 736,\n    "publisher": "Harper Collins",\n    "req_type": "Required",\n    "title": "A Testament of Hope: The Essential Writings and Speeches of Martin Luther King, Jr."\n}'], 'courses': []}

        response = self.client.get('/buy/autocomplete/', {'search': search})
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, expected_results)

class LoginTest(TestCase):
    def test_login_success(self):
        test_user = User.objects.create(
            username = "", 
            password="", 
            first_name="", 
            last_name="", 
            email="",
            is_staff=False,
            date_joined = timezone.now(),
            balance = 0.0
            )
        context = {
            'logged_in': self.client.login(username = test_user.email)
        }
        self.assertTrue(context)

@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class UserModelTest(TestCase):
    def test_user_no_edge_cases(self):
        test_user = User.objects.create(
            username = "rc8yw",
            password = "12345",
            first_name = "Rohan",
            last_name = "Chandra",
            email = "rc8yw@virginia.edu",
            is_staff = False,
            date_joined = timezone.now(),
            balance = 0.0,
        )
        self.assertEqual(test_user.username, "rc8yw")
        self.assertEqual(test_user.password, "12345")
        self.assertEqual(test_user.first_name, "Rohan")
        self.assertEqual(test_user.last_name, "Chandra")
        self.assertEqual(test_user.email, "rc8yw@virginia.edu")
        self.assertFalse(test_user.is_staff)
        self.assertEqual(test_user.balance, 0.0)
    def test_user_charFields(self):
        test_user = User.objects.create(
            username = 1,
            password = "12345",
            first_name = "Rohan",
            last_name = "Chandra",
            email = "rc8yw@virginia.edu",
            is_staff = False,
            date_joined = timezone.now(),
            balance = 0.0,
        )
        self.assertEqual(type(test_user.username), int) 
        test_user.save() 
        retrieved_user = User.objects.get(username = 1)
        self.assertEqual(retrieved_user, test_user)
        self.assertEqual(type(retrieved_user.username), str)
    def test_user_change_value_invalid(self): #This test fails
        test_user = User(
            username = "rc8yw",
            password = "12345",
            first_name = "Rohan",
            last_name = "Chandra",
            email = "rc8yw@virginia.edu",
            is_staff = False,
            date_joined = timezone.now(),
            balance = 0.0,
        )
        test_user.save()
        test_user.username = 1.456
        test_user.save()
        self.assertEqual(type(test_user.username), float) #Originally was str instead of float
    def test_login(self):
        User.objects.create_user(
            username = "rc8yw",
            password='12345',
            first_name = "Rohan",
            last_name = "Chandra",
            email = "rc8yw@virginia.edu",
            is_staff = False,
            date_joined = timezone.now(),
            balance = 0.0,
        )
        c = Client()
        self.assertTrue(c.login(username = "rc8yw@virginia.edu", password="12345"))
    def test_name_and_email_on_account_page(self):
        test_user = User.objects.create_user(
            username = "rc8yw",
            password = "12345",
            first_name = "Rohan",
            last_name = "Chandra",
            email = "rc8yw@virginia.edu",
            is_staff = False,
            date_joined = timezone.now(),
            balance = 0.0,
        )
        c = Client()
        logged_in = c.login(username = "rc8yw@virginia.edu", password="12345")
        self.assertTrue(logged_in)
        self.assertTrue(test_user.is_authenticated)
        response = c.get('/accounts/', secure = True, follow = True)
        self.assertEqual(response.status_code, 200)
        self.assertInHTML(test_user.first_name + ' ' + test_user.last_name, response.content.decode())
        self.assertInHTML(test_user.email, response.content.decode())

class SellTest(TestCase): #Can't simulate a fake photo
    def test_sell_form_valid(self):
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b'
        )
        form_data = {
            'book_title': 'sample_title',
            'book_author': 'sample_author',
            'isbn': '1234567891234',
            'book_condition': "likenew",
            'price': 1.0,
            'comments': 'sample_comment',
        }
        picture_data = {
            "picture": SimpleUploadedFile(name="small.gif", content=small_gif, content_type="image/gif"),
        }
        form = SellForm(form_data, picture_data)
        self.assertTrue(form.is_valid())
    def test_new_listing_in_current_posts(self):
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b'
        )
        form_data = {
            'book_title': 'Classical Mechanics',
            'book_author': 'John R. Taylor',
            'isbn': '9781891389221',
            'book_condition': "likenew",
            'price': 1.0,
            'comments': 'sample_comment',
        }
        picture_data = {
            "picture": SimpleUploadedFile(name="small.gif", content=small_gif, content_type="image/gif"),
        }
        form = SellForm(form_data, picture_data)
        self.assertTrue(form.is_valid())
        '''newProduct = form.save() # need to call the sell page after logging in to do this

        c = Client()
        response = c.get('/buy/9781891389221/ClassicalMechanics/', secure = True, follow = True)
        self.assertEqual(response.status_code, 200)
        self.assertInHTML("$1.0", response.content.decode())
        self.assertInHTML("Like New", response.content.decode())'''
    
        

#test models
#create one in code and check and see if they are what I am expecting
#test functionality. Build form requests import .forms, build a form and save it. 
#query the database, try to break the database with wierd values

#do the models and controllers work?

#You can see if user has been added to the database
#You can add a user, then change a value to be invalid, and then see if the same user remains, but the same data hasnt been parsed