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
        search = "Physics For Scientists and Engineers"
        expected_results = {
            "search": "Physics For Scientists and Engineers",
            "books": [
                "{\n    \"_state\": {\n        \"adding\": false,\n        \"db\": \"default\"\n    },\n    \"author\": \"['Douglas C. Giancoli']\",\n    \"bookstore_isbn\": \"0-13-613922-1\",\n    \"bookstore_new_price\": 294.11,\n    \"bookstore_used_price\": 244.5,\n    \"cover_photo\": \"\",\n    \"cover_photo_url\": \"https://images.isbndb.com/covers/92/25/9780136139225.jpg\",\n    \"date\": \"2008\",\n    \"description\": \"\",\n    \"google_rating\": 0.0,\n    \"isbn10\": \"0136139221\",\n    \"isbn13\": \"9780136139225\",\n    \"num_reviews\": 0,\n    \"page_count\": 9998,\n    \"publisher\": \"Pearson\",\n    \"req_type\": \"Pick One\",\n    \"title\": \"Physics For Scientists And Engineers With Modern Physics And Mastering Physics (4th Edition)\"\n}",
                "{\n    \"_state\": {\n        \"adding\": false,\n        \"db\": \"default\"\n    },\n    \"author\": \"['Douglas C. Giancoli', 'Addison-Wesley', 'William S Addison Wesley Higher Education', 'David P Pearson Education', 'Willoughby H Pearson Education']\",\n    \"bookstore_isbn\": \"0-321-63651-1\",\n    \"bookstore_new_price\": 129.4,\n    \"bookstore_used_price\": 109.99,\n    \"cover_photo\": \"\",\n    \"cover_photo_url\": \"{'smallThumbnail': 'http://books.google.com/books/content?id=ue6pngEACAAJ&printsec=frontcover&img=1&zoom=5&source=gbs_api', 'thumbnail': 'http://books.google.com/books/content?id=ue6pngEACAAJ&printsec=frontcover&img=1&zoom=1&source=gbs_api'}\",\n    \"date\": \"2009-06-02\",\n    \"description\": \"\",\n    \"google_rating\": 0.0,\n    \"isbn10\": \"0321636511\",\n    \"isbn13\": \"9780321636515\",\n    \"num_reviews\": 0,\n    \"page_count\": 0,\n    \"publisher\": \"Addison-Wesley\",\n    \"req_type\": \"Pick One\",\n    \"title\": \"Physics for Scientists and Engineers with Modern Physics\"\n}"],
            "courses": []
        }

        response = self.client.get('/buy/autocomplete/', {'search': search})

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            expected_results
        )

    def test_number_1(self):
        search = "12"

        #limited to 6 of each
        expected_results = {
            "search": "12",
            "books": [
                "{\n    \"_state\": {\n        \"adding\": false,\n        \"db\": \"default\"\n    },\n    \"author\": \"['Thornton Wilder']\",\n    \"bookstore_isbn\": \"0-06-051263-6\",\n    \"bookstore_new_price\": 14.99,\n    \"bookstore_used_price\": 7.45,\n    \"cover_photo\": \"\",\n    \"cover_photo_url\": \"{'smallThumbnail': 'http://books.google.com/books/content?id=8NmKkgrmj5EC&printsec=frontcover&img=1&zoom=5&edge=curl&source=gbs_api', 'thumbnail': 'http://books.google.com/books/content?id=8NmKkgrmj5EC&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api'}\",\n    \"date\": \"2003-09-23\",\n    \"description\": \"Our Town was first produced and published in 1938 to wide acclaim. This Pulitzer Prize\\u2013winning drama of life in the town of Grover 's Corners, an allegorical representation of all life, has become a classic. It is Thornton Wilder's most renowned and most frequently performed play. It is now reissued in this handsome hardcover edition, featuring a new Foreword by Donald Margulies, who writes, \\\"You are holding in your hands a great American play. Possibly the great American play.\\\" In addition, Tappan Wilder has written an eye-opening new Afterword, which includes Thornton Wilder's unpublished notes and other illuminating photographs and documentary material.\",\n    \"google_rating\": 4.5,\n    \"isbn10\": \"0060512636\",\n    \"isbn13\": \"9780060512637\",\n    \"num_reviews\": 2,\n    \"page_count\": 208,\n    \"publisher\": \"Harper Collins\",\n    \"req_type\": \"Required\",\n    \"title\": \"Our Town: A Play in Three Acts\"\n}",
                "{\n    \"_state\": {\n        \"adding\": false,\n        \"db\": \"default\"\n    },\n    \"author\": \"['Martin Luther King']\",\n    \"bookstore_isbn\": \"0-06-064691-8\",\n    \"bookstore_new_price\": 29.99,\n    \"bookstore_used_price\": 14.91,\n    \"cover_photo\": \"\",\n    \"cover_photo_url\": \"{'smallThumbnail': 'http://books.google.com/books/content?id=mTb_yAEACAAJ&printsec=frontcover&img=1&zoom=5&source=gbs_api', 'thumbnail': 'http://books.google.com/books/content?id=mTb_yAEACAAJ&printsec=frontcover&img=1&zoom=1&source=gbs_api'}\",\n    \"date\": \"1990-12-07\",\n    \"description\": \"\\\"We've got some difficult days ahead,\\\" civil rights activist Martin Luther King, Jr., told a crowd gathered at Memphis's Clayborn Temple on April 3, 1968. \\\"But it really doesn't matter to me now because I've been to the mountaintop. . . . And I've seen the promised land. I may not get there with you. But I want you to know tonight that we as a people will get to the promised land.\\\" These prohetic words, uttered the day before his assassination, challenged those he left behind to see that his \\\"promised land\\\" of racial equality became a reality; a reality to which King devoted the last twelve years of his life. These words and other are commemorated here in the only major one-volume collection of this seminal twentieth-century American prophet's writings, speeches, interviews, and autobiographical reflections. A Testament of Hope contains Martin Luther King, Jr.'s essential thoughts on nonviolence, social policy, integration, black nationalism, the ethics of love and hope, and more.\",\n    \"google_rating\": 4.0,\n    \"isbn10\": \"0060646918\",\n    \"isbn13\": \"9780060646912\",\n    \"num_reviews\": 3,\n    \"page_count\": 736,\n    \"publisher\": \"Harper Collins\",\n    \"req_type\": \"Required\",\n    \"title\": \"A Testament of Hope: The Essential Writings and Speeches of Martin Luther King, Jr.\"\n}",
                "{\n    \"_state\": {\n        \"adding\": false,\n        \"db\": \"default\"\n    },\n    \"author\": \"['Gabriel Garcia Marquez']\",\n    \"bookstore_isbn\": \"0-06-112009-X\",\n    \"bookstore_new_price\": 18.99,\n    \"bookstore_used_price\": 9.43,\n    \"cover_photo\": \"\",\n    \"cover_photo_url\": \"\",\n    \"date\": \"2006-05-30\",\n    \"description\": \"Tells the story of the Buendia family, set against the background of the evolution and eventual decadence of a small South American town.\",\n    \"google_rating\": 4.0,\n    \"isbn10\": \"006112009X\",\n    \"isbn13\": \"9780061120091\",\n    \"num_reviews\": 169,\n    \"page_count\": 448,\n    \"publisher\": \"Harper Perennial Modern Classics\",\n    \"req_type\": \"Required\",\n    \"title\": \"One Hundred Years of Solitude\"\n}",  
                "{\n    \"_state\": {\n        \"adding\": false,\n        \"db\": \"default\"\n    },\n    \"author\": \"['Alexis De Tocqueville']\",\n    \"bookstore_isbn\": \"0-06-112792-2\",\n    \"bookstore_new_price\": 22.99,\n    \"bookstore_used_price\": 11.43,\n    \"cover_photo\": \"\",\n    \"cover_photo_url\": \"https://images.isbndb.com/covers/79/22/9780061127922.jpg\",\n    \"date\": \"2006-08-29\",\n    \"description\": \"Alexis De Tocqueville ; Edited By J.p. Mayer ; Translated By George Lawrence. Originally Published: New York : Harper & Row, 1966. First Perrennial Library Edition Published 1988--title Page Verso. First Perrennial Classics Edition Published 2000--title Page Verso. First Harper Perrennial Modern Classics Edition Published 2006--title Page Verso. Includes Bibliographical References And Index.\",\n    \"google_rating\": 0.0,\n    \"isbn10\": \"0061127922\",\n    \"isbn13\": \"9780061127922\",\n    \"num_reviews\": 0,\n    \"page_count\": 777,\n    \"publisher\": \"Harper Perennial Modern Classics\",\n    \"req_type\": \"Required\",\n    \"title\": \"Democracy In America (harper Perennial Modern Classics)\"\n}",
                "{\n    \"_state\": {\n        \"adding\": false,\n        \"db\": \"default\"\n    },\n    \"author\": \"['Edward H. Carr']\",\n    \"bookstore_isbn\": \"0-06-131122-7\",\n    \"bookstore_new_price\": 15.99,\n    \"bookstore_used_price\": 11.94,\n    \"cover_photo\": \"\",\n    \"cover_photo_url\": \"{'smallThumbnail': 'http://books.google.com/books/content?id=w6fBzdPffHsC&printsec=frontcover&img=1&zoom=5&edge=curl&source=gbs_api', 'thumbnail': 'http://books.google.com/books/content?id=w6fBzdPffHsC&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api'}\",\n    \"date\": \"1964-03-25\",\n    \"description\": \"E. H. Carr's classic work on international relations published in 1939 was immediately recognized by friend and foe alike as a defining work. The author was one of the most influential and controversial intellectuals of the 20th century. The issues and themes he developed continue to have relevance to modern day concerns with power and its distribution in the international system. Michael Cox's critical introduction provides the reader with background information about the author, the context for the book, and its main themes and contemporary relevance.\",\n    \"google_rating\": 4.0,\n    \"isbn10\": \"0061311227\",\n    \"isbn13\": \"9780061311222\",\n    \"num_reviews\": 3,\n    \"page_count\": 256,\n    \"publisher\": \"Harper Collins\",\n    \"req_type\": \"Required\",\n    \"title\": \"Twenty Years' Crisis, 1919-1939\"\n}",
                "{\n    \"_state\": {\n        \"adding\": false,\n        \"db\": \"default\"\n    },\n    \"author\": \"['Morris W. Hirsch', 'Stephen Smale', 'Robert L. Devaney']\",\n    \"bookstore_isbn\": \"0-12-382010-3\",\n    \"bookstore_new_price\": 99.95,\n    \"bookstore_used_price\": 66.97,\n    \"cover_photo\": \"\",\n    \"cover_photo_url\": \"{'smallThumbnail': 'http://books.google.com/books/content?id=csYhsrOEh_MC&printsec=frontcover&img=1&zoom=5&edge=curl&source=gbs_api', 'thumbnail': 'http://books.google.com/books/content?id=csYhsrOEh_MC&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api'}\",\n    \"date\": \"2013\",\n    \"description\": \"Hirsch, Devaney, and Smale's classic Differential Equations, Dynamical Systems, and an Introduction to Chaos has been used by professors as the primary text for undergraduate and graduate level courses covering differential equations. It provides a theoretical approach to dynamical systems and chaos written for a diverse student population among the fields of mathematics, science, and engineering. Prominent experts provide everything students need to know about dynamical systems as students seek to develop sufficient mathematical skills to analyze the types of differential equations that arise in their area of study. The authors provide rigorous exercises and examples clearly and easily by slowly introducing linear systems of differential equations. Calculus is required as specialized advanced topics not usually found in elementary differential equations courses are included, such as exploring the world of discrete dynamical systems and describing chaotic systems. Classic text by three of the world's most prominent mathematicians Continues the tradition of expository excellence Contains updated material and expanded applications for use in applied studies\",\n    \"google_rating\": 0.0,\n    \"isbn10\": \"0123820103\",\n    \"isbn13\": \"9780123820105\",\n    \"num_reviews\": 0,\n    \"page_count\": 418,\n    \"publisher\": \"Academic Press\",\n    \"req_type\": \"Required\",\n    \"title\": \"Differential Equations, Dynamical Systems, and an Introduction to Chaos\"\n}"
            ],
            "courses": [
                "{\n    \"_state\": {\n        \"adding\": false,\n        \"db\": \"default\"\n    },\n    \"class_info\": \"COMM3120-ALL\",\n    \"class_term\": \"2020EUVA\",\n    \"class_title\": \"Intermediate Accounting II\",\n    \"course_code\": \"3120\",\n    \"department\": \"COMM\",\n    \"professor\": \"THAYER, JANE\",\n    \"section_number\": \"ALL\"\n}",
                "{\n    \"_state\": {\n        \"adding\": false,\n        \"db\": \"default\"\n    },\n    \"class_info\": \"ASTR1210-1\",\n    \"class_term\": \"2020EUVA\",\n    \"class_title\": \"Intro Sky and Solar System\",\n    \"course_code\": \"1210\",\n    \"department\": \"ASTR\",\n    \"professor\": \"CLEEVES,LAUREN\",\n    \"section_number\": \"1\"\n}",
                "{\n    \"_state\": {\n        \"adding\": false,\n        \"db\": \"default\"\n    },\n    \"class_info\": \"APMA3120-1\",\n    \"class_term\": \"2020EUVA\",\n    \"class_title\": \"Statistics\",\n    \"course_code\": \"3120\",\n    \"department\": \"APMA\",\n    \"professor\": \"LARK, JAMES\",\n    \"section_number\": \"1\"\n}",
                "{\n    \"_state\": {\n        \"adding\": false,\n        \"db\": \"default\"\n    },\n    \"class_info\": \"STAT2120-ALL\",\n    \"class_term\": \"2020EUVA\",\n    \"class_title\": \"Intro to Statistical Analysis\",\n    \"course_code\": \"2120\",\n    \"department\": \"STAT\",\n    \"professor\": \"ROSS\",\n    \"section_number\": \"ALL\"\n}",
                "{\n    \"_state\": {\n        \"adding\": false,\n        \"db\": \"default\"\n    },\n    \"class_info\": \"CS1112-1\",\n    \"class_term\": \"2020EUVA\",\n    \"class_title\": \"Introduction to Programming\",\n    \"course_code\": \"1112\",\n    \"department\": \"CS\",\n    \"professor\": \"COHOON\",\n    \"section_number\": \"1\"\n}",
                "{\n    \"_state\": {\n        \"adding\": false,\n        \"db\": \"default\"\n    },\n    \"class_info\": \"PLCP3012-100\",\n    \"class_term\": \"2020EUVA\",\n    \"class_title\": \"Politics of Developing Areas\",\n    \"course_code\": \"3012\",\n    \"department\": \"PLCP\",\n    \"professor\": \"FATTON\",\n    \"section_number\": \"100\"\n}"
            ]
        }

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
        search = "9780321712592"

        #just expecting the single correct book
        expected_results = {
            "search": "9780321712592",
            "books": [
                "{\n    \"_state\": {\n        \"adding\": false,\n        \"db\": \"default\"\n    },\n    \"author\": \"['Douglas C. Giancoli']\",\n    \"bookstore_isbn\": \"0-321-71259-5\",\n    \"bookstore_new_price\": 217.64,\n    \"bookstore_used_price\": 198.72,\n    \"cover_photo\": \"\",\n    \"cover_photo_url\": \"https://images.isbndb.com/covers/25/92/9780321712592.jpg\",\n    \"date\": \"2009\",\n    \"description\": \"\",\n    \"google_rating\": 0.0,\n    \"isbn10\": \"0321712595\",\n    \"isbn13\": \"9780321712592\",\n    \"num_reviews\": 0,\n    \"page_count\": 9998,\n    \"publisher\": \"Pearson\",\n    \"req_type\": \"Pick One\",\n    \"title\": \"Physics For Scientists & Engineers With Modern Physics, Books A La Carte Plus Mastering Physics (4th Edition)\"\n}"],
            "courses": []
        }

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
        form = SellForm(data = {
            'book_title': "Digital Logic Design",
            'book_author': "Frank Vahid",
            'isbn': "9781234567890",
            'book_condition': "likenew",
            'price': 100.00,
        })
        self.assertTrue(form.is_valid())
    def test_new_listing_in_current_posts(self):
        image_path = "./textbook_exchange/static/textbook_exchange/images/barcode.png"
        form = SellForm(data = {
            'book_title': 'sample_title',
            'book_author': 'sample_author',
            'isbn': '1234567891234',
            'book_condition': "likenew",
            'price': 1.00,
            'picture': UploadedFile(open(image_path, 'rb')),
            'comments': 'sample_comment',
        })
        self.assertTrue(form.is_valid())
        newProduct = form.save()
        
    
        

#test models
#create one in code and check and see if they are what I am expecting
#test functionality. Build form requests import .forms, build a form and save it. 
#query the database, try to break the database with wierd values

#do the models and controllers work?

#You can see if user has been added to the database
#You can add a user, then change a value to be invalid, and then see if the same user remains, but the same data hasnt been parsed