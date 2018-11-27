from unittest import TestCase
from app.mastermind import *

class TestMastermind(TestCase):

    def test_codemaker_feedback_value_error(self):
        with self.assertRaises(ValueError):
            codemaker = CodeMaker()
            codemaker.feedback(Guess(''))

    def test_codemaker_feedback(self):
        try:
            codemaker = CodeMaker()
            codemaker.feedback(Guess('1234'))
        except ValueError:
            self.fail('Unexpected ValueError')

    def test_guess_is_valid(self):
        guess = Guess('1234')
        self.assertEqual(guess.is_valid(), True)

    def test_guess_is_empty(self):
        guess = Guess('')
        self.assertEqual(guess.is_valid(), False)

    def test_guess_has_incorrect_length(self):
        guess = Guess('123456')
        self.assertEqual(guess.is_valid(), False)

    def test_guess_has_incorrect_value(self):
        guess = Guess('test')
        self.assertEqual(guess.is_valid(), False)

    def test_guess_has_incorrect_pattern(self):
        guess = Guess('1238')
        self.assertEqual(guess.is_valid(), False)