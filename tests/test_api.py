from unittest import TestCase
from requests import get, put

class TestAPI(TestCase):

    def setUp(self):
        self.create_uri = 'http://localhost:5000/create/'
        self.update_uri = 'http://localhost:5000/guess/'
        self.token = get(self.create_uri).json().get('token')

    def test_create_game(self):
        test = get(self.create_uri)
        self.assertEqual(test.status_code, 201)

    def test_game_token(self):
        test = get(self.create_uri)
        token = test.json().get('token', 'NA')
        test = put(self.update_uri, data={
            'code': '1234',
            'token': token
        })
        self.assertEqual(test.json().get('token'), token)

    def test_guess_without_token(self):
        test = put(self.update_uri, data={
            'code': '1234'
        })
        self.assertEqual(test.status_code, 403)

    def test_guess_without_code(self):
        test = put(self.update_uri, data={
            'token': self.token
        })
        self.assertEqual(test.status_code, 400)

    def test_guess_with_code_and_token(self):
        code = '1234'
        test = put(self.update_uri, data={
            'code': code,
            'token': self.token
        })
        self.assertEqual(test.status_code, 200)
        self.assertEqual(test.json().get('message')[-4:], code)
