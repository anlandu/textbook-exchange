from django.test import TestCase
from django.test import Client
from textbook_exchange.models import User, Class, Textbook, ProductListing
from django.utils import timezone
from django.core.exceptions import ValidationError
from textbook_exchange.forms import *
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files import File
from django.urls import *
from . import *
from django.test import Client, override_settings
from unittest.mock import MagicMock, Mock

class HelloWord(TestCase):

    def test_two_plus_two(self):
        """
        Stub test -- all tests musts start with test_
        """
        self.assertEqual(2+2, 4)
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
                "{\n    \"_state\": {\n        \"adding\": false,\n        \"db\": \"default\"\n    },\n    \"author\": \"['Leland Hartwell, Dr.', 'Michael L. Goldberg, Professor Dr.', 'Leroy Hood, Dr.']\",\n    \"bookstore_isbn\": \"978-1-260-04121-7\",\n    \"bookstore_new_price\": 166.76,\n    \"bookstore_used_price\": 141.75,\n    \"cover_photo\": \"\",\n    \"cover_photo_url\": \"{'smallThumbnail': 'http://books.google.com/books/content?id=Lb-iswEACAAJ&printsec=frontcover&img=1&zoom=5&source=gbs_api', 'thumbnail': 'http://books.google.com/books/content?id=Lb-iswEACAAJ&printsec=frontcover&img=1&zoom=1&source=gbs_api'}\",\n    \"date\": \"2017-09-21\",\n    \"description\": \"Genetics: From Genes to Genomes is a cutting-edge, introductory genetics text authored by an unparalleled author team, including Nobel Prize winner, Leland Hartwell. This edition continues to build upon the integration of Mendelian and molecular principles, providing students with the links between the early understanding of genetics and the new molecular discoveries that have changed the way the field of genetics is viewed. Users who purchase Connect receive access to the full online eBook version of the textbook as well as SmartBook.\",\n    \"google_rating\": 0.0,\n    \"isbn10\": \"1260041212\",\n    \"isbn13\": \"9781260041217\",\n    \"num_reviews\": 0,\n    \"page_count\": 848,\n    \"publisher\": \"McGraw-Hill Education\",\n    \"req_type\": \"Pick One\",\n    \"title\": \"Loose Leaf for Genetics: From Genes to Genomes\"\n}",
                "{\n    \"_state\": {\n        \"adding\": false,\n        \"db\": \"default\"\n    },\n    \"author\": \"['Stephen Abbott']\",\n    \"bookstore_isbn\": \"978-1-4939-2712-8\",\n    \"bookstore_new_price\": 32.79,\n    \"bookstore_used_price\": 0.0,\n    \"cover_photo\": \"\",\n    \"cover_photo_url\": \"{'smallThumbnail': 'http://books.google.com/books/content?id=p1t1CQAAQBAJ&printsec=frontcover&img=1&zoom=5&edge=curl&source=gbs_api', 'thumbnail': 'http://books.google.com/books/content?id=p1t1CQAAQBAJ&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api'}\",\n    \"date\": \"2015-05-19\",\n    \"description\": \"This lively introductory text exposes the student to the rewards of a rigorous study of functions of a real variable. In each chapter, informal discussions of questions that give analysis its inherent fascination are followed by precise, but not overly formal, developments of the techniques needed to make sense of them. By focusing on the unifying themes of approximation and the resolution of paradoxes that arise in the transition from the finite to the infinite, the text turns what could be a daunting cascade of definitions and theorems into a coherent and engaging progression of ideas. Acutely aware of the need for rigor, the student is much better prepared to understand what constitutes a proper mathematical proof and how to write one. Fifteen years of classroom experience with the first edition of Understanding Analysis have solidified and refined the central narrative of the second edition. Roughly 150 new exercises join a selection of the best exercises from the first edition, and three more project-style sections have been added. Investigations of Euler\\u2019s computation of \\u03b6(2), the Weierstrass Approximation Theorem, and the gamma function are now among the book\\u2019s cohort of seminal results serving as motivation and payoff for the beginning student to master the methods of analysis.\",\n    \"google_rating\": 0.0,\n    \"isbn10\": \"1493927124\",\n    \"isbn13\": \"9781493927128\",\n    \"num_reviews\": 0,\n    \"page_count\": 312,\n    \"publisher\": \"Springer\",\n    \"req_type\": \"Optional\",\n    \"title\": \"Understanding Analysis\"\n}",
                "{\n    \"_state\": {\n        \"adding\": false,\n        \"db\": \"default\"\n    },\n    \"author\": \"['Isabel Allende']\",\n    \"bookstore_isbn\": \"978-84-9759-251-2\",\n    \"bookstore_new_price\": 23.95,\n    \"bookstore_used_price\": 18.0,\n    \"cover_photo\": \"\",\n    \"cover_photo_url\": \"https://images.isbndb.com/covers/25/12/9788497592512.jpg\",\n    \"date\": \"2003\",\n    \"description\": \"\",\n    \"google_rating\": 0.0,\n    \"isbn10\": \"8497592514\",\n    \"isbn13\": \"9788497592512\",\n    \"num_reviews\": 0,\n    \"page_count\": 286,\n    \"publisher\": \"French And European Publications Inc\",\n    \"req_type\": \"Required\",\n    \"title\": \"Eva Luna (spanish Edition)\"\n}",
                "{\n    \"_state\": {\n        \"adding\": false,\n        \"db\": \"default\"\n    },\n    \"author\": \"['Steve Almond']\",\n    \"bookstore_isbn\": \"978-1-61219-491-2\",\n    \"bookstore_new_price\": 12.75,\n    \"bookstore_used_price\": 6.7,\n    \"cover_photo\": \"\",\n    \"cover_photo_url\": \"https://images.isbndb.com/covers/49/12/9781612194912.jpg\",\n    \"date\": \"2014\",\n    \"description\": \"\",\n    \"google_rating\": 0.0,\n    \"isbn10\": \"1612194915\",\n    \"isbn13\": \"9781612194912\",\n    \"num_reviews\": 0,\n    \"page_count\": 208,\n    \"publisher\": \"Melville House\",\n    \"req_type\": \"Required\",\n    \"title\": \"Against Football: One Fan's Reluctant Manifesto\"\n}",
                "{\n    \"_state\": {\n        \"adding\": false,\n        \"db\": \"default\"\n    },\n    \"author\": \"['Margaret A. Newman']\",\n    \"bookstore_isbn\": \"0-7637-1277-9\",\n    \"bookstore_new_price\": 123.95,\n    \"bookstore_used_price\": 92.9,\n    \"cover_photo\": \"\",\n    \"cover_photo_url\": \"{'smallThumbnail': 'http://books.google.com/books/content?id=_3tdBVdalroC&printsec=frontcover&img=1&zoom=5&edge=curl&source=gbs_api', 'thumbnail': 'http://books.google.com/books/content?id=_3tdBVdalroC&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api'}\",\n    \"date\": \"2000-09\",\n    \"description\": \"For the author of this book, disease is not an \\\"enemy\\\" that strikes a \\\"victim.\\\" Rather, health and disease comprise a unitary whole of individual and environment. Health as Expanding Consciousness is an inspiration to those seeking a full experience of personal health.\",\n    \"google_rating\": 4.0,\n    \"isbn10\": \"0763712779\",\n    \"isbn13\": \"9780763712778\",\n    \"num_reviews\": 1,\n    \"page_count\": 200,\n    \"publisher\": \"Jones & Bartlett Learning\",\n    \"req_type\": \"Recommended\",\n    \"title\": \"Health as Expanding Consciousness\"\n}",
                "{\n    \"_state\": {\n        \"adding\": false,\n        \"db\": \"default\"\n    },\n    \"author\": \"['Wheeler Winston Dixon', 'Gwendolyn Audrey Foster']\",\n    \"bookstore_isbn\": \"978-0-8135-9512-2\",\n    \"bookstore_new_price\": 37.95,\n    \"bookstore_used_price\": 28.33,\n    \"cover_photo\": \"\",\n    \"cover_photo_url\": \"https://images.isbndb.com/covers/51/22/9780813595122.jpg\",\n    \"date\": \"2018\",\n    \"description\": \"\",\n    \"google_rating\": 0.0,\n    \"isbn10\": \"0813595126\",\n    \"isbn13\": \"9780813595122\",\n    \"num_reviews\": 0,\n    \"page_count\": 524,\n    \"publisher\": \"Rutgers University Press\",\n    \"req_type\": \"Required\",\n    \"title\": \"A Short History Of Film, Third Edition\"\n}"],
            "courses": [
                "{\n    \"_state\": {\n        \"adding\": false,\n        \"db\": \"default\"\n    },\n    \"class_info\": \"COMM3120-ALL\",\n    \"class_term\": \"2020EUVA\",\n    \"course_code\": \"3120\",\n    \"department\": \"COMM\",\n    \"professor\": \"THAYER, JANE\",\n    \"section_number\": \"ALL\"\n}",
                "{\n    \"_state\": {\n        \"adding\": false,\n        \"db\": \"default\"\n    },\n    \"class_info\": \"ASTR1210-1\",\n    \"class_term\": \"2020EUVA\",\n    \"course_code\": \"1210\",\n    \"department\": \"ASTR\",\n    \"professor\": \"CLEEVES,LAUREN\",\n    \"section_number\": \"1\"\n}",
                "{\n    \"_state\": {\n        \"adding\": false,\n        \"db\": \"default\"\n    },\n    \"class_info\": \"APMA3120-1\",\n    \"class_term\": \"2020EUVA\",\n    \"course_code\": \"3120\",\n    \"department\": \"APMA\",\n    \"professor\": \"LARK, JAMES\",\n    \"section_number\": \"1\"\n}",
                "{\n    \"_state\": {\n        \"adding\": false,\n        \"db\": \"default\"\n    },\n    \"class_info\": \"EDIS5012-500\",\n    \"class_term\": \"2020EUVA\",\n    \"course_code\": \"5012\",\n    \"department\": \"EDIS\",\n    \"professor\": \"JENNINGS, PATRICIA\",\n    \"section_number\": \"500\"\n}",
                "{\n    \"_state\": {\n        \"adding\": false,\n        \"db\": \"default\"\n    },\n    \"class_info\": \"STAT3120-2\",\n    \"class_term\": \"2020EUVA\",\n    \"course_code\": \"3120\",\n    \"department\": \"STAT\",\n    \"professor\": \"VARANYAK\",\n    \"section_number\": \"2\"\n}",
                "{\n    \"_state\": {\n        \"adding\": false,\n        \"db\": \"default\"\n    },\n    \"class_info\": \"PLCP3012-100\",\n    \"class_term\": \"2020EUVA\",\n    \"course_code\": \"3012\",\n    \"department\": \"PLCP\",\n    \"professor\": \"FATTON\",\n    \"section_number\": \"100\"\n}"]
            }

        response = self.client.get('/buy/autocomplete/', {'search': search})

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            expected_results
        )
    
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
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            expected_results
        )

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
    def test_sell_form_invalid(self):
        form = SellForm(data = {
            'book_title': "Digital Logic Design",
            'book_author': "Frank Vahid",
            'isbn': "978-123-456-7890",
            'book_condition': "likenew",
            'price': 100.00,
        })
        self.assertFalse(form.is_valid())
    def test_new_listing_in_current_posts(self):
        mock = Mock()
        file_mock = mock.Mock(spec = File, name = 'mockFile.png')
        form = SellForm(data = {
            'book_title': 'sample_title',
            'book_author': 'sample_author',
            'isbn': 'sample_isbn',
            'book_condition': "likenew",
            'price': 1.00,
            'picture': file_mock,
            'comments': 'sample_comment',
        })
        self.assertTrue(form.is_valid())
    
        

#test models
#create one in code and check and see if they are what I am expecting
#test functionality. Build form requests import .forms, build a form and save it. 
#query the database, try to break the database with wierd values

#do the models and controllers work?

#You can see if user has been added to the database
#You can add a user, then change a value to be invalid, and then see if the same user remains, but the same data hasnt been parsed