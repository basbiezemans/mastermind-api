from random import randint
from datetime import datetime

class Game:
    def __init__(self, codemaker, codebreaker, turns=10):
        self.codemaker = codemaker
        self.codebreaker = codebreaker
        self.created = datetime.utcnow()
        self.turns = turns
        self.turn_counter = 0

    def reset(self):
        self.turn_counter = 0
        self.codemaker.initialize()

    def process(self, feedback):
        """ Determines the result of a game turn
        """
        self.turn_counter += 1
        if feedback.result.is_correct():
            self.codebreaker.add_point()
        elif self.has_no_turns_left():
            self.codemaker.add_point()

    def has_no_turns_left(self):
        return self.turn_counter == self.turns

    def __repr__(self):
        return (
            f'Game(codemaker={self.codemaker}'
            f', codebreaker={self.codebreaker}, turns={self.turns})'
        )

class Player:
    def __init__(self):
        self.points = 0

    def add_point(self):
        self.points += 1

    def __repr__(self):
        return 'Player()'

class CodeMaker(Player):
    def __init__(self, code=None):
        super().__init__()
        if code is None:
            self.initialize()
        else:
            self.pattern = [int(c) for c in code]

    def initialize(self):
        """ Creates a random pattern of four digits between 1 and 6 (inclusive)
        """
        self.pattern = [randint(1,6) for _ in range(4)]

    def evaluate(self, guess):
        """ Evaluates the guess and returns a list of ones and zeros for correct digits
        """
        digits = [int(c) for c in guess.code]
        result = []
        pattern = self.pattern[:]
        for i in range(4):
            digit = digits[i]
            if digit == self.pattern[i]:
                result.insert(0, 1)
                pattern.remove(digit)
            elif digit in pattern:
                result.append(0)
                pattern.remove(digit)
        return self.EvaluationResult(result)

    class EvaluationResult:
        def __init__(self, value):
            self.value = value
        def is_correct(self):
            return sum(self.value) == 4

    def feedback(self, guess):
        """ Returns a Feedback object or raises a ValueError
        """
        if guess.is_valid():
            result = self.evaluate(guess)
            return Feedback(guess, result)
        else:
            raise ValueError('Invalid Guess')

    def __repr__(self):
        return 'CodeMaker()'

class CodeBreaker(Player):
    def __init__(self):
        super().__init__()

    def guess(self, code):
        """ Returns a Guess object
        """
        return Guess(code)

    def __repr__(self):
        return 'CodeBreaker()'

class Guess:
    def __init__(self, code):
        self.code = code

    def is_valid(self):
        """ Returns True if this is a valid guess and False otherwise
        """
        if self.code is None:
            return False
        if len(self.code) != 4:
            return False
        try:
            int(self.code)
        except ValueError:
            return False
        for c in self.code:
            n = int(c)
            if n < 1 or n > 6:
                return False
        return True

    def __repr__(self):
        return f'Guess(code={self.code})'

class Feedback:
    def __init__(self, guess, result):
        self.code = guess.code
        self.result = result
        self.response = result.value

    def __repr__(self):
        return f'Feedback(guess={self.code}, result={self.response})'