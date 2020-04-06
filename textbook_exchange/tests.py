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
            'isbn': "978-123-456-7890",
            'book_condition': "likenew",
            'price': 100.00,
        })
        self.assertTrue(form.is_valid())
    def test_new_listing_in_current_posts(self):
        image_path = "./textbook_exchange/static/textbook_exchange/images/barcode.png"
        form = SellForm(data = {
            'book_title': 'sample_title',
            'book_author': 'sample_author',
            'isbn': 'sample_isbn',
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