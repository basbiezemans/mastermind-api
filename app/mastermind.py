from random import randint
from secrets import token_hex
from datetime import datetime

class Game:
    def __init__(self, codemaker, codebreaker, turns=10):
        self.codemaker = codemaker
        self.codebreaker = codebreaker
        self.created = datetime.utcnow()
        self.counter = LimitCounter(turns)

    def update(self, code):
        guess = self.codebreaker.guess(code)
        feedback = self.codemaker.feedback(guess)
        self.process(feedback)
        return feedback

    def turn_count(self):
        return (self.counter.value, self.counter.limit)

    def score(self):
        return (self.codemaker.points, self.codebreaker.points)

    def over(self):
        return self.counter.reached_limit()
    
    def reset(self):
        self.counter.reset()
        self.codemaker.initialize()

    def process(self, result):
        """ Increment the turn count and, if applicable, award a point to the winning player.
        """
        self.counter.increment()
        if result.is_correct():
            self.codebreaker.add_point()
        elif self.counter.reached_limit():
            self.codemaker.add_point()

    def __repr__(self):
        return (
            f'Game(codemaker={self.codemaker}'
            f', codebreaker={self.codebreaker}, turns={self.counter.limit})'
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
        """ Create a random pattern of four digits between 1 and 6 (inclusive).
        """
        self.pattern = [randint(1,6) for _ in range(4)]

    def evaluate(self, guess):
        """ Evaluate the guess and return an EvaluationResult object.
        """
        code1 = [int(c) for c in guess.code]
        code2 = self.pattern[:]
        ones = []; zeros = []
        digits = []; pattern = []
        for i in range(4):
            digit1 = code1[i]
            digit2 = code2[i]
            if digit1 == digit2:
                ones.append(1)
            else:
                digits.append(digit1)
                pattern.append(digit2)
        for digit in digits:
            if digit in pattern:
                zeros.append(0)
                pattern.remove(digit)
        return EvaluationResult(ones + zeros)

    def feedback(self, guess):
        """ Return an EvaluationResult object or raise a ValueError.
        """
        if guess.is_valid():
            return self.evaluate(guess)
        else:
            raise ValueError('Invalid Guess')

    def __repr__(self):
        return 'CodeMaker()'

class CodeBreaker(Player):
    def __init__(self):
        super().__init__()

    def guess(self, code):
        """ Return a Guess object.
        """
        return Guess(code)

    def __repr__(self):
        return 'CodeBreaker()'

class Guess:
    def __init__(self, code):
        self.code = code

    def is_valid(self):
        """ Return True if this is a valid guess and False otherwise.
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

class EvaluationResult:
    def __init__(self, value):
        self.value = value

    def is_correct(self):
        return self.value == [1,1,1,1]

    def __repr__(self):
        return f'EvaluationResult(value={self.value})'

class LimitCounter:
    def __init__(self, limit):
        self.limit = limit
        self.value = 0

    def reset(self):
        self.value = 0

    def increment(self):
        if not self.reached_limit():
            self.value += 1

    def reached_limit(self):
        return self.value == self.limit

    def __repr__(self):
        return f'LimitCounter(limit={self.limit})'

class GameRepository:
    def __init__(self):
        self.games = {}

    def store(self, game):
        """ Store a Game object and return its token.
        """
        token = token_hex(20)
        self.games[token] = game
        return token

    def has(self, token):
        """ Return True if token is in repository and False otherwise. 
        """
        return token in self.games

    def retrieve(self, token):
        """ Return a Game object or raise a KeyError.
        """
        return self.games[token]

    def remove(self, token):
        """ Remove a Game object or raise a KeyError.
        """
        del self.games[token]
