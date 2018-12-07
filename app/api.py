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
        games[token] = Game(CodeMaker(), CodeBreaker())
        return {
            'message': 'A new game has been created. Good luck!',
            'token': token
        }, 201

    def patch(self, token=None):
        """ Updates a game and returns feedback
        """
        if token not in games:
            return abort(404)
        game = games.get(token)
        guess = game.codebreaker.guess(request.form.get('code'))
        try:
            feedback = game.codemaker.feedback(guess)
        except ValueError:
            return abort(400)
        else:
            game.process(feedback)
            correct_guess = feedback.result.is_correct()
            if correct_guess or game.counter.reached_limit():
                result = 'You won!' if correct_guess else 'You lost.'
                message = (
                    f'{result} The current score is {game.codebreaker.points} '
                    f'(You) vs {game.codemaker.points} (CodeMaker). Try again.'
                )
                game.reset()
            else:
                message = (
                    f'Guess {game.counter.value} of {game.counter.limit}. '
                    f'You guessed: {guess.code}'
                )
            return {
                'message': message,
                'token': token,
                'feedback': feedback.keybits
            }

    def get(self, token=None):
        """ Returns information about a game
        """
        if token not in games:
            return abort(404)
        game = games.get(token)
        return {
            'message': f'This game was created on {game.created}',
            'token': token,
            'score': {
                'codemaker': game.codemaker.points,
                'codebreaker': game.codebreaker.points
            }
        }

    def delete(self, token=None):
        """ Deletes a game and doesn't return any content
        """
        if token not in games:
            return abort(404)
        del games[token]
        return '', 204

# Endpoint
api.add_resource(Mastermind, '/game/', '/game/<token>')

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')