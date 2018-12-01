from unittest import TestCase
from requests import get, put

class TestAPI(TestCase):

    def setUp(self):
        game = get('http://localhost:5000/create/')
        self.token = game.json().get('token')

    def test_create_game(self):
        test = get('http://localhost:5000/create/')
        self.assertEqual(test.status_code, 201)

    def test_game_token(self):
        test = get('http://localhost:5000/create/')
        token = test.json().get('token', 'NA')
        test = put('http://localhost:5000/guess/', data={
            'code': '1234',
            'token': token
        })
        self.assertEqual(test.json().get('token'), token)

    def test_guess_without_token(self):
        test = put('http://localhost:5000/guess/', data={
            'code': '1234'
        })
        self.assertEqual(test.status_code, 403)

    def test_guess_without_code(self):
        test = put('http://localhost:5000/guess/', data={
            'token': self.token
        })
        self.assertEqual(test.status_code, 400)

    def test_guess_with_code_and_token(self):
        code = '1234'
        test = put('http://localhost:5000/guess/', data={
            'code': code,
            'token': self.token
        })
        self.assertEqual(test.status_code, 200)
        self.assertEqual(test.json().get('message')[-4:], code)
