from django.test import TestCase
from django.test import Client


class HelloWord(TestCase):

    def test_two_plus_two(self):
        """
        Stub test -- all tests musts start with test_
        """
        self.assertEqual(2+2, 4)

class AutocompleteTest(TestCase):

    '''
    Since we don't have all the books and courses in yet I don't know what
    the results will be but this is the format for the autocomplete tests
    '''
    def test_template(self):quiarch})

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            expected_results
        )
