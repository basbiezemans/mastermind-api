from unittest import TestCase
from requests import get, put

class TestAPI(TestCase):
    
    def test_create_game(self):
        test = get('http://localhost:5000/create/')
        self.assertEqual(test.status_code, 200)

    def test_guess_without_pattern(self):
        test = put('http://localhost:5000/guess/', data={})
        self.assertEqual(test.status_code, 400)

    def test_guess_pattern(self):
        guess = {
            'pattern': 'BLANK'
        }
        test = put('http://localhost:5000/guess/', data=guess)
        self.assertEqual(test.status_code, 200)
        self.assertEqual(test.json().get('message'), 'You guessed: BLANK')
