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
        self.assertEqual(ordered(json.loads(response.content)), ordered(expected_results))


    def test_title_1(self):
        search = "Physics For Scientists"
        expected_results = {'search': 'Physics For Scientists', 'books': ['{\n    "_state": {\n        "adding": false,\n        "db": "default"\n    },\n    "author": "[\'Douglas C. Giancoli\']",\n    "bookstore_isbn": "0-321-71259-5",\n    "bookstore_new_price": 217.64,\n    "bookstore_used_price": 198.72,\n    "cover_photo": "",\n    "cover_photo_url": "https://images.isbndb.com/covers/25/92/9780321712592.jpg",\n    "date": "2009",\n    "description": "",\n    "google_rating": 0.0,\n    "isbn10": "0321712595",\n    "isbn13": "9780321712592",\n    "num_reviews": 0,\n    "page_count": 9998,\n    "publisher": "Pearson",\n    "req_type": "Pick One",\n    "title": "Physics For Scientists & Engineers With Modern Physics, Books A La Carte Plus Mastering Physics (4th Edition)"\n}', '{\n    "_state": {\n        "adding": false,\n        "db": "default"\n    },\n    "author": "[\'Douglas C. Giancoli\', \'Addison-Wesley\', \'William S Addison Wesley Higher Education\', \'David P Pearson Education\', \'Willoughby H Pearson Education\']",\n    "bookstore_isbn": "0-321-63651-1",\n    "bookstore_new_price": 129.4,\n    "bookstore_used_price": 109.99,\n    "cover_photo": "",\n    "cover_photo_url": "{\'smallThumbnail\': \'http://books.google.com/books/content?id=ue6pngEACAAJ&printsec=frontcover&img=1&zoom=5&source=gbs_api\', \'thumbnail\': \'http://books.google.com/books/content?id=ue6pngEACAAJ&printsec=frontcover&img=1&zoom=1&source=gbs_api\'}",\n    "date": "2009-06-02",\n    "description": "",\n    "google_rating": 0.0,\n    "isbn10": "0321636511",\n    "isbn13": "9780321636515",\n    "num_reviews": 0,\n    "page_count": 0,\n    "publisher": "Addison-Wesley",\n    "req_type": "Pick One",\n    "title": "Physics for Scientists and Engineers with Modern Physics"\n}', '{\n    "_state": {\n        "adding": false,\n        "db": "default"\n    },\n    "author": "[\'Douglas C. Giancoli\']",\n    "bookstore_isbn": "0-13-613922-1",\n    "bookstore_new_price": 294.11,\n    "bookstore_used_price": 244.5,\n    "cover_photo": "",\n    "cover_photo_url": "https://images.isbndb.com/covers/92/25/9780136139225.jpg",\n    "date": "2008",\n    "description": "",\n    "google_rating": 0.0,\n    "isbn10": "0136139221",\n    "isbn13": "9780136139225",\n    "num_reviews": 0,\n    "page_count": 9998,\n    "publisher": "Pearson",\n    "req_type": "Pick One",\n    "title": "Physics For Scientists And Engineers With Modern Physics And Mastering Physics (4th Edition)"\n}'], 'courses': []}
        response = self.client.get('/buy/autocomplete/', {'search': search})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(ordered(json.loads(response.content)), ordered(expected_results))

    def test_number_1(self):
        search = "123"
        expected_results = {'search': '123', 'books': ['{\n    "_state": {\n        "adding": false,\n        "db": "default"\n    },\n    "author": "[\'Andrew L. Chaikin\', \'Tom Hanks\']",\n    "bookstore_isbn": "978-0-14-311235-8",\n    "bookstore_new_price": 22.0,\n    "bookstore_used_price": 16.5,\n    "cover_photo": "",\n    "cover_photo_url": "https://images.isbndb.com/covers/23/58/9780143112358.jpg",\n    "date": "August 2007",\n    "description": "This acclaimed portrait of heroism and ingenuity captures a watershed moment in human history. The astronauts themselves have called it the definitive account of their missions. On the night of July 20, 1969, our world changed forever when Neil Armstrong and Buzz Aldrin walked on the moon. Based on in-depth interviews with twenty-three of the twenty-four moon voyagers, as well as those who struggled to get the program moving, <i>A Man on the Moon</i> conveys every aspect of the Apollo missions with breathtaking immediacy and stunning detail. <h3>Publishers Weekly</h3> Scheduled to coincide with the 25th anniversary of the first lunar landing on July 20, 1969, this chronicle offers a comprehensive, often penetrating look at NASA\'s Apollo program. Originating in 1961, when President John Kennedy told Congress that the U.S. should attempt to land a man on the moon ``before this decade is out,\'\' the program\'s last mission ended in December, 1972, with the splashdown of Apollo 17. Diary-like reports mix with first- and third-person accounts as Chaikin, an editor at Sky And Telescope magazine, delivers a chronological view of the missions and those who planned and flew them. Focusing closely on the Apollo astronauts, including Buzz Aldrin, Pete Conrad and Neil Armstrong, Chaikin gives his topic a sense of immediacy. But his treatment, lengthy as it is, reads more like an extended magazine article. Missing is a view of Apollo in a wider context, one that captures the mythos of our efforts to land on the moon. (June)",\n    "google_rating": 0.0,\n    "isbn10": "014311235X",\n    "isbn13": "9780143112358",\n    "num_reviews": 0,\n    "page_count": 720,\n    "publisher": "Penguin Group (USA)",\n    "req_type": "Required",\n    "title": "a-man-on-the-moon"\n}', '{\n    "_state": {\n        "adding": false,\n        "db": "default"\n    },\n    "author": "[\'Stephen White\', \'Richard Sakwa\', \'Henry E. Hale\']",\n    "bookstore_isbn": "978-0-8223-5812-1",\n    "bookstore_new_price": 26.95,\n    "bookstore_used_price": 13.91,\n    "cover_photo": "",\n    "cover_photo_url": "{\'smallThumbnail\': \'http://books.google.com/books/content?id=z0-xoAEACAAJ&printsec=frontcover&img=1&zoom=5&source=gbs_api\', \'thumbnail\': \'http://books.google.com/books/content?id=z0-xoAEACAAJ&printsec=frontcover&img=1&zoom=1&source=gbs_api\'}",\n    "date": "2014-09-01",\n    "description": "The eighth edition of a popular course book tracking recent developments in Russian politics.",\n    "google_rating": 0.0,\n    "isbn10": "0822358123",\n    "isbn13": "9780822358121",\n    "num_reviews": 0,\n    "page_count": 320,\n    "publisher": "",\n    "req_type": "Required",\n    "title": "Developments in Russian Politics 8"\n}', '{\n    "_state": {\n        "adding": false,\n        "db": "default"\n    },\n    "author": "[\'Morris W. Hirsch\', \'Stephen Smale\', \'Robert L. Devaney\']",\n    "bookstore_isbn": "0-12-382010-3",\n    "bookstore_new_price": 99.95,\n    "bookstore_used_price": 66.97,\n    "cover_photo": "",\n    "cover_photo_url": "{\'smallThumbnail\': \'http://books.google.com/books/content?id=csYhsrOEh_MC&printsec=frontcover&img=1&zoom=5&edge=curl&source=gbs_api\', \'thumbnail\': \'http://books.google.com/books/content?id=csYhsrOEh_MC&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api\'}",\n    "date": "2013",\n    "description": "Hirsch, Devaney, and Smale\'s classic Differential Equations, Dynamical Systems, and an Introduction to Chaos has been used by professors as the primary text for undergraduate and graduate level courses covering differential equations. It provides a theoretical approach to dynamical systems and chaos written for a diverse student population among the fields of mathematics, science, and engineering. Prominent experts provide everything students need to know about dynamical systems as students seek to develop sufficient mathematical skills to analyze the types of differential equations that arise in their area of study. The authors provide rigorous exercises and examples clearly and easily by slowly introducing linear systems of differential equations. Calculus is required as specialized advanced topics not usually found in elementary differential equations courses are included, such as exploring the world of discrete dynamical systems and describing chaotic systems. Classic text by three of the world\'s most prominent mathematicians Continues the tradition of expository excellence Contains updated material and expanded applications for use in applied studies",\n    "google_rating": 0.0,\n    "isbn10": "0123820103",\n    "isbn13": "9780123820105",\n    "num_reviews": 0,\n    "page_count": 418,\n    "publisher": "Academic Press",\n    "req_type": "Required",\n    "title": "Differential Equations, Dynamical Systems, and an Introduction to Chaos"\n}', '{\n    "_state": {\n        "adding": false,\n        "db": "default"\n    },\n    "author": "[\'Morris W. Hirsch\', \'Stephen Smale\', \'Robert L. Devaney\']",\n    "bookstore_isbn": "978-0-12-382011-2",\n    "bookstore_new_price": 41.98,\n    "bookstore_used_price": 0.0,\n    "cover_photo": "",\n    "cover_photo_url": "{\'smallThumbnail\': \'http://books.google.com/books/content?id=rly1AAmAXh8C&printsec=frontcover&img=1&zoom=5&edge=curl&source=gbs_api\', \'thumbnail\': \'http://books.google.com/books/content?id=rly1AAmAXh8C&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api\'}",\n    "date": "2012-03-12",\n    "description": "Hirsch, Devaney, and Smale\\u2019s classic Differential Equations, Dynamical Systems, and an Introduction to Chaos has been used by professors as the primary text for undergraduate and graduate level courses covering differential equations. It provides a theoretical approach to dynamical systems and chaos written for a diverse student population among the fields of mathematics, science, and engineering. Prominent experts provide everything students need to know about dynamical systems as students seek to develop sufficient mathematical skills to analyze the types of differential equations that arise in their area of study. The authors provide rigorous exercises and examples clearly and easily by slowly introducing linear systems of differential equations. Calculus is required as specialized advanced topics not usually found in elementary differential equations courses are included, such as exploring the world of discrete dynamical systems and describing chaotic systems. Classic text by three of the world\\u2019s most prominent mathematicians Continues the tradition of expository excellence Contains updated material and expanded applications for use in applied studies",\n    "google_rating": 0.0,\n    "isbn10": "0123820111",\n    "isbn13": "9780123820112",\n    "num_reviews": 0,\n    "page_count": 432,\n    "publisher": "Academic Press",\n    "req_type": "Optional",\n    "title": "Differential Equations, Dynamical Systems, and an Introduction to Chaos"\n}', '{\n    "_state": {\n        "adding": false,\n        "db": "default"\n    },\n    "author": "[\'Nicholas Evans\']",\n    "bookstore_isbn": "0-631-23306-7",\n    "bookstore_new_price": 49.75,\n    "bookstore_used_price": 37.13,\n    "cover_photo": "",\n    "cover_photo_url": "https://images.isbndb.com/covers/30/60/9780631233060.jpg",\n    "date": "2009-04-27",\n    "description": "\\"The next century will see more than half of the world\'s 6,000 languages become extinct. Most of these will disappear without being adequately recorded. Yet each distills the philosophy, knowledge, and cultural fabric of a different people. This compelling book asks what loss to our collective intellectual heritage will be inflicted by the death of these languages. This book: Explores the unique philosophy, knowledge, and cultural assumptions of languages, and their impact on our collective intellectual heritage -- Questions why such linguistic diversity exists in the first place, and how can we best respond to the challenge of recording and documenting these fragile oral traditions while they are still with us -- Brings conceptual issues vividly to life by weaving in portraits of individual ?last speakers? and anecdotes about linguists and their discoveries.\\" -- from publisher.",\n    "google_rating": 0.0,\n    "isbn10": "0631233067",\n    "isbn13": "9780631233060",\n    "num_reviews": 0,\n    "page_count": 310,\n    "publisher": "Wiley-blackwell",\n    "req_type": "Required",\n    "title": "Dying Words: Endangered Languages And What They Have To Tell Us"\n}', '{\n    "_state": {\n        "adding": false,\n        "db": "default"\n    },\n    "author": "[\'Alicia Giralt\']",\n    "bookstore_isbn": "1-61233-113-0",\n    "bookstore_new_price": 61.19,\n    "bookstore_used_price": 48.95,\n    "cover_photo": "",\n    "cover_photo_url": "{\'smallThumbnail\': \'http://books.google.com/books/content?id=nICWCgAAQBAJ&printsec=frontcover&img=1&zoom=5&edge=curl&source=gbs_api\', \'thumbnail\': \'http://books.google.com/books/content?id=nICWCgAAQBAJ&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api\'}",\n    "date": "2012-09",\n    "description": "This innovative textbook fulfills the needs of upper-division Spanish students who are pursuing degrees in the health professions, plan to become medical interpreters or just want to improve their proficiency in the language. It provides multiple opportunities to learn vocabulary related to the medical field, reviews hard-to-understand grammatical concepts, describes health-related cultural competence and presents opportunities to discuss issues of concern about the health of Hispanic communities in the US and abroad.",\n    "google_rating": 0.0,\n    "isbn10": "1612331130",\n    "isbn13": "9781612331133",\n    "num_reviews": 0,\n    "page_count": 330,\n    "publisher": "Universal-Publishers",\n    "req_type": "Required",\n    "title": "Espa\\u00f1ol M\\u00e9dico Y Sociedad: Un Libro Para Estudiantes de Espa\\u00f1ol en El Tercer A\\u00f1o de Estudios"\n}'], 'courses': ['{\n    "_state": {\n        "adding": false,\n        "db": "default"\n    },\n    "class_info": "ASTR1230-100",\n    "class_term": "2020EUVA",\n    "class_title": "Intro Astronomical Observation",\n    "course_code": "1230",\n    "department": "ASTR",\n    "professor": "MAJEWSKI,STEVEN",\n    "section_number": "100"\n}']}
        response = self.client.get('/buy/autocomplete/', {'search': search})
        self.assertEqual(response.status_code, 200)
        r_j = json.loads(response.content)
        r_j['books'].sort()
        expected_results['books'].sort()
        self.assertEqual(r_j, expected_results)

    
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
        self.assertEqual(ordered(json.loads(response.content)), ordered(expected_results))


    def test_invalid_isbn(self):
        search = "999999999999"

        #should not find any correct books
        expected_results = {'search': '999999999999', 'books': [], 'courses': []}
        
        response = self.client.get('/buy/autocomplete/', {'search': search})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ordered(json.loads(response.content)), ordered(expected_results))

    def test_valid_isbn(self):
        search = "9780060646912"

        #just expecting the single correct book
        expected_results = {'search': '9780060646912', 'books': ['{\n    "_state": {\n        "adding": false,\n        "db": "default"\n    },\n    "author": "[\'Martin Luther King\']",\n    "bookstore_isbn": "0-06-064691-8",\n    "bookstore_new_price": 29.99,\n    "bookstore_used_price": 14.91,\n    "cover_photo": "",\n    "cover_photo_url": "{\'smallThumbnail\': \'http://books.google.com/books/content?id=mTb_yAEACAAJ&printsec=frontcover&img=1&zoom=5&source=gbs_api\', \'thumbnail\': \'http://books.google.com/books/content?id=mTb_yAEACAAJ&printsec=frontcover&img=1&zoom=1&source=gbs_api\'}",\n    "date": "1990-12-07",\n    "description": "\\"We\'ve got some difficult days ahead,\\" civil rights activist Martin Luther King, Jr., told a crowd gathered at Memphis\'s Clayborn Temple on April 3, 1968. \\"But it really doesn\'t matter to me now because I\'ve been to the mountaintop. . . . And I\'ve seen the promised land. I may not get there with you. But I want you to know tonight that we as a people will get to the promised land.\\" These prohetic words, uttered the day before his assassination, challenged those he left behind to see that his \\"promised land\\" of racial equality became a reality; a reality to which King devoted the last twelve years of his life. These words and other are commemorated here in the only major one-volume collection of this seminal twentieth-century American prophet\'s writings, speeches, interviews, and autobiographical reflections. A Testament of Hope contains Martin Luther King, Jr.\'s essential thoughts on nonviolence, social policy, integration, black nationalism, the ethics of love and hope, and more.",\n    "google_rating": 4.0,\n    "isbn10": "0060646918",\n    "isbn13": "9780060646912",\n    "num_reviews": 3,\n    "page_count": 736,\n    "publisher": "Harper Collins",\n    "req_type": "Required",\n    "title": "A Testament of Hope: The Essential Writings and Speeches of Martin Luther King, Jr."\n}'], 'courses': []}
        
        response = self.client.get('/buy/autocomplete/', {'search': search})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ordered(json.loads(response.content)), ordered(expected_results))

    def test_isbn10_with_dashes(self):
        search = "0-06-064691-8"

        #just expecting the single correct book
        expected_results = {'search': '0-06-064691-8', 'books': ['{\n    "_state": {\n        "adding": false,\n        "db": "default"\n    },\n    "author": "[\'Martin Luther King\']",\n    "bookstore_isbn": "0-06-064691-8",\n    "bookstore_new_price": 29.99,\n    "bookstore_used_price": 14.91,\n    "cover_photo": "",\n    "cover_photo_url": "{\'smallThumbnail\': \'http://books.google.com/books/content?id=mTb_yAEACAAJ&printsec=frontcover&img=1&zoom=5&source=gbs_api\', \'thumbnail\': \'http://books.google.com/books/content?id=mTb_yAEACAAJ&printsec=frontcover&img=1&zoom=1&source=gbs_api\'}",\n    "date": "1990-12-07",\n    "description": "\\"We\'ve got some difficult days ahead,\\" civil rights activist Martin Luther King, Jr., told a crowd gathered at Memphis\'s Clayborn Temple on April 3, 1968. \\"But it really doesn\'t matter to me now because I\'ve been to the mountaintop. . . . And I\'ve seen the promised land. I may not get there with you. But I want you to know tonight that we as a people will get to the promised land.\\" These prohetic words, uttered the day before his assassination, challenged those he left behind to see that his \\"promised land\\" of racial equality became a reality; a reality to which King devoted the last twelve years of his life. These words and other are commemorated here in the only major one-volume collection of this seminal twentieth-century American prophet\'s writings, speeches, interviews, and autobiographical reflections. A Testament of Hope contains Martin Luther King, Jr.\'s essential thoughts on nonviolence, social policy, integration, black nationalism, the ethics of love and hope, and more.",\n    "google_rating": 4.0,\n    "isbn10": "0060646918",\n    "isbn13": "9780060646912",\n    "num_reviews": 3,\n    "page_count": 736,\n    "publisher": "Harper Collins",\n    "req_type": "Required",\n    "title": "A Testament of Hope: The Essential Writings and Speeches of Martin Luther King, Jr."\n}'], 'courses': []}
        
        response = self.client.get('/buy/autocomplete/', {'search': search})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ordered(json.loads(response.content)), ordered(expected_results))

    def test_isbn10_without_dashes(self):
        search = "0060646918"

        #just expecting the single correct book
        expected_results = {'search': '0060646918', 'books': ['{\n    "_state": {\n        "adding": false,\n        "db": "default"\n    },\n    "author": "[\'Martin Luther King\']",\n    "bookstore_isbn": "0-06-064691-8",\n    "bookstore_new_price": 29.99,\n    "bookstore_used_price": 14.91,\n    "cover_photo": "",\n    "cover_photo_url": "{\'smallThumbnail\': \'http://books.google.com/books/content?id=mTb_yAEACAAJ&printsec=frontcover&img=1&zoom=5&source=gbs_api\', \'thumbnail\': \'http://books.google.com/books/content?id=mTb_yAEACAAJ&printsec=frontcover&img=1&zoom=1&source=gbs_api\'}",\n    "date": "1990-12-07",\n    "description": "\\"We\'ve got some difficult days ahead,\\" civil rights activist Martin Luther King, Jr., told a crowd gathered at Memphis\'s Clayborn Temple on April 3, 1968. \\"But it really doesn\'t matter to me now because I\'ve been to the mountaintop. . . . And I\'ve seen the promised land. I may not get there with you. But I want you to know tonight that we as a people will get to the promised land.\\" These prohetic words, uttered the day before his assassination, challenged those he left behind to see that his \\"promised land\\" of racial equality became a reality; a reality to which King devoted the last twelve years of his life. These words and other are commemorated here in the only major one-volume collection of this seminal twentieth-century American prophet\'s writings, speeches, interviews, and autobiographical reflections. A Testament of Hope contains Martin Luther King, Jr.\'s essential thoughts on nonviolence, social policy, integration, black nationalism, the ethics of love and hope, and more.",\n    "google_rating": 4.0,\n    "isbn10": "0060646918",\n    "isbn13": "9780060646912",\n    "num_reviews": 3,\n    "page_count": 736,\n    "publisher": "Harper Collins",\n    "req_type": "Required",\n    "title": "A Testament of Hope: The Essential Writings and Speeches of Martin Luther King, Jr."\n}'], 'courses': []}
        
        response = self.client.get('/buy/autocomplete/', {'search': search})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ordered(json.loads(response.content)), ordered(expected_results))

    def test_isbn_type_int(self):
        search = 9780060646912

        #just expecting the single correct book
        expected_results = {'search': '9780060646912', 'books': ['{\n    "_state": {\n        "adding": false,\n        "db": "default"\n    },\n    "author": "[\'Martin Luther King\']",\n    "bookstore_isbn": "0-06-064691-8",\n    "bookstore_new_price": 29.99,\n    "bookstore_used_price": 14.91,\n    "cover_photo": "",\n    "cover_photo_url": "{\'smallThumbnail\': \'http://books.google.com/books/content?id=mTb_yAEACAAJ&printsec=frontcover&img=1&zoom=5&source=gbs_api\', \'thumbnail\': \'http://books.google.com/books/content?id=mTb_yAEACAAJ&printsec=frontcover&img=1&zoom=1&source=gbs_api\'}",\n    "date": "1990-12-07",\n    "description": "\\"We\'ve got some difficult days ahead,\\" civil rights activist Martin Luther King, Jr., told a crowd gathered at Memphis\'s Clayborn Temple on April 3, 1968. \\"But it really doesn\'t matter to me now because I\'ve been to the mountaintop. . . . And I\'ve seen the promised land. I may not get there with you. But I want you to know tonight that we as a people will get to the promised land.\\" These prohetic words, uttered the day before his assassination, challenged those he left behind to see that his \\"promised land\\" of racial equality became a reality; a reality to which King devoted the last twelve years of his life. These words and other are commemorated here in the only major one-volume collection of this seminal twentieth-century American prophet\'s writings, speeches, interviews, and autobiographical reflections. A Testament of Hope contains Martin Luther King, Jr.\'s essential thoughts on nonviolence, social policy, integration, black nationalism, the ethics of love and hope, and more.",\n    "google_rating": 4.0,\n    "isbn10": "0060646918",\n    "isbn13": "9780060646912",\n    "num_reviews": 3,\n    "page_count": 736,\n    "publisher": "Harper Collins",\n    "req_type": "Required",\n    "title": "A Testament of Hope: The Essential Writings and Speeches of Martin Luther King, Jr."\n}'], 'courses': []}
        
        response = self.client.get('/buy/autocomplete/', {'search': search})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ordered(json.loads(response.content)), ordered(expected_results))

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
        decoded_response=response.content.decode()
        self.assertEqual(response.status_code, 200)
        self.assertInHTML(test_user.first_name + ' ' + test_user.last_name, decoded_response)
        self.assertInHTML(test_user.email, decoded_response)

@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class SellTest(TestCase): #Can't simulate a fake photo
    fixtures = ['testing_data/textbooks.json', 'testing_data/classes.json']
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

    def test_sell_form_three_decimal_price(self):
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b'
        )
        form_data = {
            'book_title': 'sample_title_1',
            'book_author': 'sample_author_1',
            'isbn': '1234567891234',
            'book_condition': "likenew",
            'price': 1.0051,
            'comments': 'sample_comment',
        }
        picture_data = {
            "picture": SimpleUploadedFile(name="small.gif", content=small_gif, content_type="image/gif"),
        }
        form = SellForm(form_data, picture_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {'price':['Ensure that there are no more than 2 decimal places.']})

    
    def test_sell_form_string_price(self):
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b'
        )
        form_data = {
            'book_title': 'sample_title_1',
            'book_author': 'sample_author_1',
            'isbn': '1234567891234',
            'book_condition': "likenew",
            'price': "k",
            'comments': 'sample_comment',
        }
        picture_data = {
            "picture": SimpleUploadedFile(name="small.gif", content=small_gif, content_type="image/gif"),
        }
        form = SellForm(form_data, picture_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {'price':['Enter a number.']})


    def test_sell_form_blank_picture(self):
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b'
        )
        form_data = {
            'book_title': 'sample_title_1',
            'book_author': 'sample_author_1',
            'isbn': '1234567891234',
            'book_condition': "likenew",
            'price': 1.0,
            'comments': 'sample_comment',
        }
        picture_data={}
        form = SellForm(form_data, picture_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {'picture':['This field is required.']})

    def test_two_sell_forms_same_picture(self):
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b'
        )
        form_data_1 = {
            'book_title': 'sample_title_1',
            'book_author': 'sample_author_1',
            'isbn': '1234567891234',
            'book_condition': "likenew",
            'price': 1.0,
            'comments': 'sample_comment',
        }
        picture_data_1={'picture':SimpleUploadedFile(name="small.gif", content=small_gif, content_type="image/gif")}

        form_data_2 = {
            'book_title': 'sample_title_2',
            'book_author': 'sample_author_2',
            'isbn': '1234567891234',
            'book_condition': "likenew",
            'price': 1.0,
            'comments': 'sample_comment',
        }
        picture_data_2={'picture':SimpleUploadedFile(name="small.gif", content=small_gif, content_type="image/gif")}

        form_1 = SellForm(form_data_1, picture_data_1)
        form_2 = SellForm(form_data_2, picture_data_2)
        self.assertTrue(form_1.is_valid())
        self.assertTrue(form_2.is_valid())

    def test_new_listing_in_current_posts(self):
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

        pl = ProductListing.objects.create(
            user=test_user,
            textbook=Textbook.objects.get(pk="1-891389-22-X"), 
            cart=None,
            price=100.0,
            condition="likenew",
        )

        c = Client()

        c.login(username = "rc8yw@virginia.edu", password="12345")
        
        response = c.get("/accounts/", secure=True, follow=True)  
        decoded_response=response.content.decode()      
        self.assertEqual(response.status_code, 200)
        self.assertInHTML("Classical Mechanics", decoded_response)
        self.assertInHTML("$100.00", decoded_response)
        self.assertInHTML("Rohan Chandra", decoded_response)
        self.assertInHTML("Condition: Like new", decoded_response)

    def test_new_listing_in_search(self):
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
        pl = ProductListing.objects.create(
            user=test_user,
            textbook=Textbook.objects.get(pk="1-891389-22-X"), 
            cart=None,
            price=100.0,
            condition="likenew",
        )
        c = Client()
        c.login(username = "rc8yw@virginia.edu", password="12345")
        
        response = c.get("/buy/9781891389221/ClassicalMechanics/", secure=True, follow=True)  
        decoded_response=response.content.decode()      
        self.assertEqual(response.status_code, 200)
        self.assertInHTML("Classical Mechanics", decoded_response)
        self.assertInHTML("$100.00", decoded_response)
        self.assertInHTML("Rohan Chandra", decoded_response)
        self.assertInHTML("Condition: Like new", decoded_response)

    def test_listing_in_cart_not_in_search(self):
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

        test_user2 = User.objects.create_user(
            username = "nw5zp",
            password = "54321",
            first_name = "Nick",
            last_name = "Winans",
            email = "nw5zp@virginia.edu",
            is_staff = False,
            date_joined = timezone.now(),
            balance = 0.0,
        )

        pl = ProductListing.objects.create(
            user=test_user,
            textbook=Textbook.objects.get(pk="1-891389-22-X"), 
            cart=test_user.cart,
            price=100.0,
            condition="likenew",
        )

        c = Client()
        c.login(username = "nw5zp@virginia.edu", password="54321")
        response = c.get("/buy/9781891389221/ClassicalMechanics/", secure=True, follow=True)        
        self.assertEqual(response.status_code, 200)
        try:
            decoded_response=response.content.decode()
            self.assertInHTML("Classical Mechanics", decoded_response)
            self.assertInHTML("$100.00", decoded_response)
            self.assertInHTML("Rohan Chandra", decoded_response)
            self.assertInHTML("Condition: Like new", decoded_response)
            self.fail("Listing not removed when added to cart")
        except AssertionError:
            pass
        
    def test_listing_in_cart(self):
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

        pl = ProductListing.objects.create(
            user=test_user,
            textbook=Textbook.objects.get(pk="1-891389-22-X"), 
            cart=test_user.cart,
            price=100.0,
            condition="likenew",
        )

        c = Client()
        c.login(username = "rc8yw@virginia.edu", password="12345")
        response = c.get("/cart/", secure=True, follow=True)   
        decoded_response=response.content.decode()     
        self.assertEqual(response.status_code, 200)
        self.assertInHTML("Classical Mechanics", decoded_response)
        self.assertInHTML("$100.00", decoded_response)
        self.assertInHTML("remove", decoded_response)

    def test_add_listing_to_cart(self):
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

        pl = ProductListing.objects.create(
            user=test_user,
            textbook=Textbook.objects.get(pk="1-891389-22-X"), 
            cart=None,
            price=100.0,
            condition="likenew",
        )

        c = Client()
        c.login(username = "rc8yw@virginia.edu", password="12345")
        response = c.post("/cart/", {"id": pl.id, "function": "add"})        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), {'status': 'success'})

    def test_remove_listing_from_cart(self):
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

        pl = ProductListing.objects.create(
            user=test_user,
            textbook=Textbook.objects.get(pk="1-891389-22-X"), 
            cart=None,
            price=200.0,
            condition="likenew",
        )

        c = Client()
        c.login(username = "rc8yw@virginia.edu", password="12345")
        response = c.post("/cart/", {"id": pl.id, "function": "add"})        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), {'status': 'success'})
        response = c.post("/cart/", {"id": pl.id, "function": "remove"})        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), {'status': 'success'})
        response = c.get("/cart/", secure=True, follow=True)
        decoded_response=response.content.decode()
        try:
            self.assertInHTML("Classical Mechanics", decoded_response)
            self.assertInHTML("$200.00", decoded_response)
            self.assertInHTML("Rohan Chandra", decoded_response)
            self.assertInHTML("Condition: Like new", decoded_response)
            self.fail("Listing not removed from cart")
        except AssertionError:
            pass
        response = c.get("/buy/9781891389221/ClassicalMechanics/", secure=True, follow=True)
        decoded_response=response.content.decode()        
        self.assertEqual(response.status_code, 200)
        self.assertInHTML("Classical Mechanics", decoded_response)
        self.assertInHTML("$200.00", decoded_response)
        self.assertInHTML("Rohan Chandra", decoded_response)
        self.assertInHTML("Condition: Like new", decoded_response)

    def test_checkout_success(self):
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

        pl = ProductListing.objects.create(
            user=test_user,
            textbook=Textbook.objects.get(pk="1-891389-22-X"), 
            cart=None,
            price=200.0,
            condition="likenew",
        )

        c = Client()
        c.login(username = "rc8yw@virginia.edu", password="12345")
        response = c.post("/cart/", {"id": pl.id, "function": "add"})        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), {'status': 'success'})
        response = c.get("/cart/checkout/success", secure=True, follow=True)
        #self.assertInHTML("Success!", decoded_response)
        response = c.get("/buy/9781891389221/ClassicalMechanics/", secure=True, follow=True)
        decoded_response=response.content.decode()        
        self.assertEqual(response.status_code, 200)
        try:
            self.assertInHTML("Classical Mechanics", decoded_response)
            self.assertInHTML("$200.00", decoded_response)
            self.assertInHTML("Rohan Chandra", decoded_response)
            self.assertInHTML("Condition: Like new", decoded_response)
            self.fail("Listing not removed on checkout success")
        except AssertionError:
            pass
        response = c.get("/accounts/", secure=True, follow=True)
        decoded_response=response.content.decode()
        try:
            self.assertInHTML("Classical Mechanics", decoded_response)
            self.assertInHTML("$200.00", decoded_response)
            self.assertInHTML("Rohan Chandra", decoded_response)
            self.assertInHTML("Condition: Like new", decoded_response)
            self.fail("Listing not removed on checkout success")
        except AssertionError:
            pass
        response = c.get("/accounts/past_posts", secure=True, follow=True)
        decoded_response=response.content.decode()
        self.assertInHTML("Classical Mechanics", decoded_response)
        self.assertInHTML("$200.00", decoded_response)
        self.assertInHTML("Condition: Like new", decoded_response)

        

#test models
#create one in code and check and see if they are what I am expecting
#test functionality. Build form requests import .forms, build a form and save it. 
#query the database, try to break the database with weird values

#do the models and controllers work?

#You can see if user has been added to the database
#You can add a user, then change a value to be invalid, and then see if the same user remains, but the same data hasnt been parsed
def ordered(obj):
    if isinstance(obj, dict):
        return sorted((k, ordered(v)) for k, v in obj.items())
    if isinstance(obj, list):
        return sorted(ordered(x) for x in obj)
    else:
        return obj