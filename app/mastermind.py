
class CodeMaker:
    def __init__(self):
        pass

    def feedback(self, guess):
        """ Returns a Feedback object or raises a ValueError
        """
        if guess.is_valid():
            return Feedback(guess.code, [])
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
        return True if self.code == '1234' else False

    def __repr__(self):
        return 'Guess(code={self.code})'

class Feedback:
    def __init__(self, code, response):
        self.code = code
        self.response = response

    def __repr__(self):
        return f'Feedback(code={self.code}, response={self.response})'