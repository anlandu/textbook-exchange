from django.test import TestCase

class HelloWord(TestCase):

    def two_plus_two(self):
        """
        Stub test
        """
        self.assertEqual(2+2, 4)
