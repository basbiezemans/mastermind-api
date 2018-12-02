from unittest import TestCase
from requests import post, patch, get

class TestAPI(TestCase):

    def setUp(self):
        self.game_uri = 'http://localhost:5000/game/'
        self.token = post(self.game_uri).json().get('token')

    def test_create_game(self):
        test = post(self.game_uri)
        self.assertEqual(test.status_code, 201)

    def test_guess_with_token(self):
        test = patch(self.game_uri, data={
            'code': '1234',
            'token': self.token
        })
        self.assertEqual(test.json().get('token'), self.token)

    def test_guess_without_token(self):
        test = patch(self.game_uri, data={
            'code': '1234'
        })
        self.assertEqual(test.status_code, 403)

    def test_guess_without_code(self):
        test = patch(self.game_uri, data={
            'token': self.token
        })
        self.assertEqual(test.status_code, 400)

    def test_guess_with_code_and_token(self):
        code = '1234'
        test = patch(self.game_uri, data={
            'code': code,
            'token': self.token
        })
        self.assertEqual(test.status_code, 200)
        self.assertEqual(test.json().get('message')[-4:], code)

    def test_retrieve__game_information(self):
        test = get(self.game_uri + self.token)
        self.assertEqual(test.status_code, 200)
