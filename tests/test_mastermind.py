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

    def test_codemaker_provides_correct_feedback(self):
        codemaker = CodeMaker(code='6243')
        feedback = codemaker.feedback(Guess('1234'))
        # 2, 3 and 4 are correct, 2 also has the correct position
        expected = [1,0,0]
        self.assertEqual(feedback.response, expected)

    def test_codemaker_provides_correct_feedback_if_there_are_duplicates(self):
        # If there are duplicate colours in the guess, they cannot all be awarded a key peg unless 
        # they correspond to the same number of duplicate colours in the hidden code.
        codemaker = CodeMaker(code='6243')
        feedback = codemaker.feedback(Guess('6225'))
        expected = [1,1]
        self.assertEqual(feedback.response, expected)
        codemaker = CodeMaker(code='6443')
        feedback = codemaker.feedback(Guess('4124'))
        expected = [0,0]
        self.assertEqual(feedback.response, expected)

    def test_player_points(self):
        # The codemaker will earn a point if the codebreaker doesn't guess the pattern within one
        # round of the game. The winner is the one who has the most points after the agreed-upon 
        # number of games are played.
        codemaker = CodeMaker(code='1212')
        codebreaker = CodeBreaker()
        codemaker_points_before = codemaker.points
        codebreaker_points_before = codebreaker.points
        game = Game(codemaker, codebreaker, turns=1)
        game.process(codemaker.feedback(Guess('5656'))) # wrong guess
        codemaker_points_after = codemaker.points
        codebreaker_points_after = codebreaker.points
        self.assertEqual(codemaker_points_before, 0)
        self.assertEqual(codemaker_points_after, 1)
        self.assertEqual(codebreaker_points_before, 0)
        self.assertEqual(codebreaker_points_after, 0)
        # New game
        codemaker = CodeMaker(code='1212')
        codebreaker = CodeBreaker()
        codemaker_points_before = codemaker.points
        codebreaker_points_before = codebreaker.points
        game = Game(codemaker, codebreaker, turns=1)
        game.process(codemaker.feedback(Guess('1212'))) # correct guess
        codemaker_points_after = codemaker.points
        codebreaker_points_after = codebreaker.points
        self.assertEqual(codemaker_points_before, 0)
        self.assertEqual(codemaker_points_after, 0)
        self.assertEqual(codebreaker_points_before, 0)
        self.assertEqual(codebreaker_points_after, 1)

    def test_correct_number_of_games(self):
        # Must be an even number greater than 0 and less than a certain maximum.
        pass

    def test_game_terminates_correctly(self):
        pass
