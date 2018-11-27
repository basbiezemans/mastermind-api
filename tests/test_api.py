from unittest import TestCase
from requests import get, put

class TestAPI(TestCase):
    
    def test_create_game(self):
        test = get('http://localhost:5000/create/')
        self.assertEqual(test.status_code, 200)

    def test_guess_without_code(self):
        test = put('http://localhost:5000/guess/', data={})
        self.assertEqual(test.status_code, 400)

    def test_guess_code(self):
        test = put('http://localhost:5000/guess/', data={
            'code': '1234'
        })
        self.assertEqual(test.status_code, 200)
        self.assertEqual(test.json().get('message'), 'You guessed: 1234')

    def test_empty_code(self):
        test = put('http://localhost:5000/guess/', data={
            'code': ''
        })
        self.assertEqual(test.status_code, 400)

    def test_code_with_incorrect_length(self):
        test = put('http://localhost:5000/guess/', data={
            'code': '123456'
        })
        self.assertEqual(test.status_code, 400)

    def test_code_with_incorrect_value(self):
        test = put('http://localhost:5000/guess/', data={
            'code': 'test'
        })
        self.assertEqual(test.status_code, 400)

    def test_code_with_incorrect_pattern(self):
        test = put('http://localhost:5000/guess/', data={
            'code': '1238'
        })
        self.assertEqual(test.status_code, 400)