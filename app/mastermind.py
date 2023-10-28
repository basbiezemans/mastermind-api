from random import randint
from datetime import datetime
from functools import reduce
from itertools import repeat

class Game:
    def __init__(self, codemaker, codebreaker, turns=10):
        self.codemaker = codemaker
        self.codebreaker = codebreaker
        self.counter = LimitCounter(turns)
        self.created = str(datetime.utcnow())

    def update(self, code):
        guess = self.codebreaker.guess(code)
        feedback = self.codemaker.feedback(guess)
        self.process(feedback)
        return feedback

    @staticmethod
    def create():
        return Game(CodeMaker(), CodeBreaker())

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

    def __eq__(self, other):
        return self.hash() == other.hash()

    def hash(self):
        return hash((self.token, self.created) + self.score())

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

    def compare_lists(self, list1, list2):
        pairs = list(zip(list1, list2))
        unequal_pairs = [(a, b) for a, b in pairs if a != b]
        count_correct = len(pairs) - len(unequal_pairs)
        def count(acc, digit):
            tally, digits = acc
            if digit in digits:
                tally += 1
                digits.remove(digit)
            return tally, digits
        guess, secret = unzip(unequal_pairs)
        count_present = reduce(count, guess, (0, secret))[0]
        return count_correct, count_present

    def evaluate(self, guess):
        """ Evaluate the guess and return an EvaluationResult object.
        """
        list1 = [int(c) for c in guess.code]
        list2 = self.pattern[:]
        correct, present = self.compare_lists(list1, list2)
        ones = list(repeat(1, correct))
        zeros = list(repeat(0, present))
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

class GameBuilder:
    def __init__(self):
        self.game = Game.create()

    def set_token(self, token):
        self.game.token = token
        return self

    def set_timestamp(self, created):
        self.game.created = created
        return self

    def set_codemaker_score(self, points):
        self.game.codemaker.points = points
        return self

    def set_codebreaker_score(self, points):
        self.game.codebreaker.points = points
        return self

    def get_result(self):
        return self.game

def unzip(pairs):
    if not pairs:
        return [], []
    t1, t2 = zip(*pairs)
    return list(t1), list(t2)