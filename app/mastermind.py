from random import randint

class CodeMaker:
    def __init__(self, code=None):
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
        return result

    def feedback(self, guess):
        """ Returns a Feedback object or raises a ValueError
        """
        if guess.is_valid():
            result = self.evaluate(guess)
            return Feedback(guess.code, result)
        else:
            raise ValueError('Invalid Guess')

    def __repr__(self):
        return 'CodeMaker()'

class CodeBreaker:
    def __init__(self):
        pass

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
        return 'Guess(code={self.code})'

class Feedback:
    def __init__(self, code, response):
        self.code = code
        self.response = response

    def __repr__(self):
        return f'Feedback(code={self.code}, response={self.response})'