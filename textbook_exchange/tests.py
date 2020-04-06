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
        search = "Physics For Scientists"
        expected_results = {'search': 'Physics For Scientists', 'books': ['{\n    "_state": {\n        "adding": false,\n        "db": "default"\n    },\n    "author": "[\'Douglas C. Giancoli\']",\n    "bookstore_isbn": "0-321-71259-5",\n    "bookstore_new_price": 217.64,\n    "bookstore_used_price": 198.72,\n    "cover_photo": "",\n    "cover_photo_url": "https://images.isbndb.com/covers/25/92/9780321712592.jpg",\n    "date": "2009",\n    "description": "",\n    "google_rating": 0.0,\n    "isbn10": "0321712595",\n    "isbn13": "9780321712592",\n    "num_reviews": 0,\n    "page_count": 9998,\n    "publisher": "Pearson",\n    "req_type": "Pick One",\n    "title": "Physics For Scientists & Engineers With Modern Physics, Books A La Carte Plus Mastering Physics (4th Edition)"\n}', '{\n    "_state": {\n        "adding": false,\n        "db": "default"\n    },\n    "author": "[\'Douglas C. Giancoli\', \'Addison-Wesley\', \'William S Addison Wesley Higher Education\', \'David P Pearson Education\', \'Willoughby H Pearson Education\']",\n    "bookstore_isbn": "0-321-63651-1",\n    "bookstore_new_price": 129.4,\n    "bookstore_used_price": 109.99,\n    "cover_photo": "",\n    "cover_photo_url": "{\'smallThumbnail\': \'http://books.google.com/books/content?id=ue6pngEACAAJ&printsec=frontcover&img=1&zoom=5&source=gbs_api\', \'thumbnail\': \'http://books.google.com/books/content?id=ue6pngEACAAJ&printsec=frontcover&img=1&zoom=1&source=gbs_api\'}",\n    "date": "2009-06-02",\n    "description": "",\n    "google_rating": 0.0,\n    "isbn10": "0321636511",\n    "isbn13": "9780321636515",\n    "num_reviews": 0,\n    "page_count": 0,\n    "publisher": "Addison-Wesley",\n    "req_type": "Pick One",\n    "title": "Physics for Scientists and Engineers with Modern Physics"\n}', '{\n    "_state": {\n        "adding": false,\n        "db": "default"\n    },\n    "author": "[\'Douglas C. Giancoli\']",\n    "bookstore_isbn": "0-13-613922-1",\n    "bookstore_new_price": 294.11,\n    "bookstore_used_price": 244.5,\n    "cover_photo": "",\n    "cover_photo_url": "https://images.isbndb.com/covers/92/25/9780136139225.jpg",\n    "date": "2008",\n    "description": "",\n    "google_rating": 0.0,\n    "isbn10": "0136139221",\n    "isbn13": "9780136139225",\n    "num_reviews": 0,\n    "page_count": 9998,\n    "publisher": "Pearson",\n    "req_type": "Pick One",\n    "title": "Physics For Scientists And Engineers With Modern Physics And Mastering Physics (4th Edition)"\n}'], 'courses': []}
        response = self.client.get('/buy/autocomplete/', {'search': search})

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            expected_results
        )

    def test_number_1(self):
        search = "12"

        expected_results = {'search': '12', 'books': ['{\n    "_state": {\n        "adding": false,\n        "db": "default"\n    },\n    "author": "[\'Andrew L. Chaikin\', \'Tom Hanks\']",\n    "bookstore_isbn": "978-0-14-311235-8",\n    "bookstore_new_price": 22.0,\n    "bookstore_used_price": 16.5,\n    "cover_photo": "",\n    "cover_photo_url": "https://images.isbndb.com/covers/23/58/9780143112358.jpg",\n    "date": "August 2007",\n    "description": "This acclaimed portrait of heroism and ingenuity captures a watershed moment in human history. The astronauts themselves have called it the definitive account of their missions. On the night of July 20, 1969, our world changed forever when Neil Armstrong and Buzz Aldrin walked on the moon. Based on in-depth interviews with twenty-three of the twenty-four moon voyagers, as well as those who struggled to get the program moving, <i>A Man on the Moon</i> conveys every aspect of the Apollo missions with breathtaking immediacy and stunning detail. <h3>Publishers Weekly</h3> Scheduled to coincide with the 25th anniversary of the first lunar landing on July 20, 1969, this chronicle offers a comprehensive, often penetrating look at NASA\'s Apollo program. Originating in 1961, when President John Kennedy told Congress that the U.S. should attempt to land a man on the moon ``before this decade is out,\'\' the program\'s last mission ended in December, 1972, with the splashdown of Apollo 17. Diary-like reports mix with first- and third-person accounts as Chaikin, an editor at Sky And Telescope magazine, delivers a chronological view of the missions and those who planned and flew them. Focusing closely on the Apollo astronauts, including Buzz Aldrin, Pete Conrad and Neil Armstrong, Chaikin gives his topic a sense of immediacy. But his treatment, lengthy as it is, reads more like an extended magazine article. Missing is a view of Apollo in a wider context, one that captures the mythos of our efforts to land on the moon. (June)",\n    "google_rating": 0.0,\n    "isbn10": "014311235X",\n    "isbn13": "9780143112358",\n    "num_reviews": 0,\n    "page_count": 720,\n    "publisher": "Penguin Group (USA)",\n    "req_type": "Required",\n    "title": "a-man-on-the-moon"\n}', '{\n    "_state": {\n        "adding": false,\n        "db": "default"\n    },\n    "author": "[\'Reed Hundt\']",\n    "bookstore_isbn": "978-1-948122-31-3",\n    "bookstore_new_price": 22.35,\n    "bookstore_used_price": 16.8,\n    "cover_photo": "",\n    "cover_photo_url": "{\'smallThumbnail\': \'http://books.google.com/books/content?id=L7WIuAEACAAJ&printsec=frontcover&img=1&zoom=5&source=gbs_api\', \'thumbnail\': \'http://books.google.com/books/content?id=L7WIuAEACAAJ&printsec=frontcover&img=1&zoom=1&source=gbs_api\'}",\n    "date": "2019-04-02",\n    "description": "This book is the compelling story of President Obama\\u2019s domestic policy decisions made between September 2008 and his inauguration on January 20, 2009. Barack Obama determined the fate of his presidency before he took office. His momentous decisions led to Donald Trump, for Obama the worst person imaginable, taking his place eight years later. This book describes these decisions and discusses how the results could have been different. Based on dozens of interviews with actors in the Obama transition, as well as the author\\u2019s personal observations, this book provides unique commentary of those defining decisions of winter 2008\\u20132009. A decade later, the ramifications of the Great Recession and the role of government in addressing the crisis animate the ideological battle between progressivism and neoliberalism in the Democratic Party and the radical direction of the Republican Party. As many seek the presidency in the November 2020 election, all candidates and of course the eventual winner will face decisions that may be as critical and difficult as those confronted by Barack Obama. This book aims to provide the guidance of history.",\n    "google_rating": 0.0,\n    "isbn10": "1948122316",\n    "isbn13": "9781948122313",\n    "num_reviews": 0,\n    "page_count": 400,\n    "publisher": "RosettaBooks",\n    "req_type": "Required",\n    "title": "A Crisis Wasted: Barack Obama\'s Defining Decisions"\n}', '{\n    "_state": {\n        "adding": false,\n        "db": "default"\n    },\n    "author": "[\'\\u041c\\u0438\\u0445\\u0430\\u0438\\u043b \\u042e\\u0440\\u044c\\u0435\\u0432\\u0438\\u0447 \\u041b\\u0435\\u0440\\u043c\\u043e\\u043d\\u0442\\u043e\\u0432\', \'Mikhail I\\ufe20U\\ufe21r\\u02b9evich Lermontov\']",\n    "bookstore_isbn": "0-8129-7076-4",\n    "bookstore_new_price": 15.0,\n    "bookstore_used_price": 7.46,\n    "cover_photo": "",\n    "cover_photo_url": "{\'smallThumbnail\': \'http://books.google.com/books/content?id=QDaVx2wVKjkC&printsec=frontcover&img=1&zoom=5&source=gbs_api\', \'thumbnail\': \'http://books.google.com/books/content?id=QDaVx2wVKjkC&printsec=frontcover&img=1&zoom=1&source=gbs_api\'}",\n    "date": "2004",\n    "description": "I BELA I was traveling post from Tiflis. My cart\'s entire load consisted of one small valise, which was half filled with travel notes about Georgia. Of these, the greater part, fortunately for you, have been lost, and the valise containing my remaining possessions, fortunately for me, is intact. The sun was already beginning to drop behind the snowy ridge when I rode into the Koyshaur Valley. The driver, an Ossetian, drove the horses tirelessly in order to make it up Koyshaur Mountain by nightfall, singing songs at the top of his voice. A glorious spot, this valley! On every side of the mountain are impregnable reddish cliffs hung with green ivy and crowned with clusters of plane trees, yellow precipices scoured by running water, and there, high up, a golden fringe of snows, while below, the Aragva, having embraced another nameless stream gushing noisily from a black, mist-filled gorge, has stretched out like a silver thread and shimmers like a snake with scales.",\n    "google_rating": 4.0,\n    "isbn10": "0812970764",\n    "isbn13": "9780812970760",\n    "num_reviews": 23,\n    "page_count": 166,\n    "publisher": "Random House LLC",\n    "req_type": "Required",\n    "title": "A Hero of Our Time"\n}', '{\n    "_state": {\n        "adding": false,\n        "db": "default"\n    },\n    "author": "[\'Michael Cunningham\']",\n    "bookstore_isbn": "0-312-20231-8",\n    "bookstore_new_price": 18.0,\n    "bookstore_used_price": 13.64,\n    "cover_photo": "",\n    "cover_photo_url": "https://images.isbndb.com/covers/23/16/9780312202316.jpg",\n    "date": "1998",\n    "description": "",\n    "google_rating": 0.0,\n    "isbn10": "0312202318",\n    "isbn13": "9780312202316",\n    "num_reviews": 0,\n    "page_count": 352,\n    "publisher": "Picador",\n    "req_type": "Required",\n    "title": "A Home At The End Of The World: A Novel"\n}', '{\n    "_state": {\n        "adding": false,\n        "db": "default"\n    },\n    "author": "[\'Wheeler Winston Dixon\', \'Gwendolyn Audrey Foster\']",\n    "bookstore_isbn": "978-0-8135-9512-2",\n    "bookstore_new_price": 37.95,\n    "bookstore_used_price": 28.33,\n    "cover_photo": "",\n    "cover_photo_url": "https://images.isbndb.com/covers/51/22/9780813595122.jpg",\n    "date": "2018",\n    "description": "",\n    "google_rating": 0.0,\n    "isbn10": "0813595126",\n    "isbn13": "9780813595122",\n    "num_reviews": 0,\n    "page_count": 524,\n    "publisher": "Rutgers University Press",\n    "req_type": "Required",\n    "title": "A Short History Of Film, Third Edition"\n}', '{\n    "_state": {\n        "adding": false,\n        "db": "default"\n    },\n    "author": "[\'Nathan L. Essex\']",\n    "bookstore_isbn": "0-13-335191-2",\n    "bookstore_new_price": 49.99,\n    "bookstore_used_price": 38.25,\n    "cover_photo": "",\n    "cover_photo_url": "{\'smallThumbnail\': \'http://books.google.com/books/content?id=yXPrngEACAAJ&printsec=frontcover&img=1&zoom=5&source=gbs_api\', \'thumbnail\': \'http://books.google.com/books/content?id=yXPrngEACAAJ&printsec=frontcover&img=1&zoom=1&source=gbs_api\'}",\n    "date": "2014-01-23",\n    "description": "School Law and the Public Schools by Nathan L. Essex gives educators and policy makers at all levels practical, easy-to-read, relevant information on the historical and contemporary legal issues affecting the organization and administration of schools in the United States. Virtually every topic of concern to today\'s educators is covered in a practical, easy-to-read organization and style that\'s accessible even to those with little or no knowledge of the legal issues affecting public schools. Revised chapters in this new Sixth Edition include recent rulings on religion in public schools, social media, Facebook and Twitter challenges, virtual charter schools, administrators\' authority at bus stops, legal aspects of teachers and administrators\' evaluation, teacher performance and misconduct, 504 Rehabilitation plans, the McKinney-Vento Homeless Act, violence and tragedy in U.S. schools, procedures for evaluating and responding to threats, natural disasters and school safety, proposed changes to No Child Left Behind by the White House, use of chaperones for field trips, and new application exercises at the end of each chapter.",\n    "google_rating": 0.0,\n    "isbn10": "0133351912",\n    "isbn13": "9780133351910",\n    "num_reviews": 0,\n    "page_count": 240,\n    "publisher": "Pearson College Division",\n    "req_type": "Required",\n    "title": "A Teacher\'s Pocket Guide to School Law"\n}'], 'courses': ['{\n    "_state": {\n        "adding": false,\n        "db": "default"\n    },\n    "class_info": "MATH1210-ALL",\n    "class_term": "2020EUVA",\n    "class_title": "A survey of Calculus I",\n    "course_code": "1210",\n    "department": "MATH",\n    "professor": "STAFF",\n    "section_number": "ALL"\n}', '{\n    "_state": {\n        "adding": false,\n        "db": "default"\n    },\n    "class_info": "MATH1220-ALL",\n    "class_term": "2020EUVA",\n    "class_title": "A Survey of Calculus II",\n    "course_code": "1220",\n    "department": "MATH",\n    "professor": "STAFF",\n    "section_number": "ALL"\n}', '{\n    "_state": {\n        "adding": false,\n        "db": "default"\n    },\n    "class_info": "EDIS4012-1",\n    "class_term": "2020EUVA",\n    "class_title": "Adv Mindfulness Hlth & Hum Dev",\n    "course_code": "4012",\n    "department": "EDIS",\n    "professor": "JENNINGS, PATRICIA",\n    "section_number": "1"\n}', '{\n    "_state": {\n        "adding": false,\n        "db": "default"\n    },\n    "class_info": "APMA2512-1",\n    "class_term": "2020EUVA",\n    "class_title": "Advanced Topics in APMA",\n    "course_code": "2512",\n    "department": "APMA",\n    "professor": "MA, HUI",\n    "section_number": "1"\n}', '{\n    "_state": {\n        "adding": false,\n        "db": "default"\n    },\n    "class_info": "HIAF3112-1",\n    "class_term": "2020EUVA",\n    "class_title": "African Environmental History",\n    "course_code": "3112",\n    "department": "HIAF",\n    "professor": "LA FLEUR, JD",\n    "section_number": "1"\n}', '{\n    "_state": {\n        "adding": false,\n        "db": "default"\n    },\n    "class_info": "HIEU2112-100",\n    "class_term": "2020EUVA",\n    "class_title": "Britain since 1688",\n    "course_code": "2112",\n    "department": "HIEU",\n    "professor": "LINSTRUM, ERIK",\n    "section_number": "100"\n}']}
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