from flask import Flask, request
from flask_restful import Resource, Api, abort
from secrets import token_hex
from mastermind import Game, CodeMaker, CodeBreaker

app = Flask(__name__)
api = Api(app)

games = {}

class Mastermind(Resource):
    def post(self):
        """ Creates a new game and returns a token
        """
        token = token_hex(20)
        game = Game(CodeMaker(), CodeBreaker())
        games[token] = game
        return {
            'message': 'A new game has been created. Good luck!',
            'token': token
        }, 201

    def patch(self):
        """ Updates a game and returns feedback
        """
        token = request.form.get('token')
        if token not in games:
            return {
                'message': 'You first have to create a game.',
                'token': None,
                'feedback': None
            }, 403
        game = games.get(token)
        guess = game.codebreaker.guess(request.form.get('code'))
        try:
            feedback = game.codemaker.feedback(guess)
        except ValueError:
            return abort(400)
        else:
            game.process(feedback)
            if feedback.result.is_correct() or game.has_no_turns_left():
                result = 'You won!' if feedback.result.is_correct() else 'You lost.'
                message = (
                    f'{result} The current score is {game.codebreaker.points} '
                    f'(You) vs {game.codemaker.points} (CodeMaker). Try again.'
                )
                game.reset()
            else:
                message = (
                    f'Guess {game.turn_counter} of {game.turns}. '
                    f'You guessed: {guess.code}'
                )
            return {
                'message': message,
                'token': token,
                'feedback': feedback.response
            }

    def get(self, token=None):
        """ Returns information about a game
        """
        if token is None:
            return abort(400)
        if token not in games:
            return {
                'message': 'You first have to create a game.',
                'token': None,
                'score': None
            }, 403
        game = games.get(token)
        return {
            'message': f'This game was created on {game.created}',
            'token': token,
            'score': {
                'codemaker': game.codemaker.points,
                'codebreaker': game.codebreaker.points
            }
        }

# Endpoint
api.add_resource(Mastermind, '/game/', '/game/<token>')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')