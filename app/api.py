from flask import Flask, request
from flask_restful import Resource, Api, abort
from mastermind import GameRepository, Game, CodeMaker, CodeBreaker

app = Flask(__name__)
api = Api(app)

repo = GameRepository()

class Mastermind(Resource):
    def post(self):
        """ Create a new game and return a token.
        """
        token = repo.store(Game(CodeMaker(), CodeBreaker()))
        return {
            'message': 'A new game has been created. Good luck!',
            'token': token
        }, 201

    def patch(self, token=None):
        """ Update a game and return feedback.
        """
        try:
            game = repo.retrieve(token)
        except KeyError:
            return abort(404)
        guess = request.form.get('code')
        try:
            result = game.update(guess)
        except ValueError:
            return abort(400)
        correct_guess = result.is_correct()
        if correct_guess or game.over():
            codemaker_score, codebreaker_score = game.score()
            outcome = 'You won!' if correct_guess else 'You lost.'
            message = (
                f'{outcome} The current score is {codebreaker_score} '
                f'(You) vs {codemaker_score} (CodeMaker). Try again.'
            )
            game.reset()
        else:
            current, total = game.turn_count()
            message = (
                f'Guess {current} of {total}. '
                f'You guessed: {guess}'
            )
        return {
            'message': message,
            'token': token,
            'feedback': result.value
        }

    def get(self, token=None):
        """ Return information about a game.
        """
        try:
            game = repo.retrieve(token)
        except KeyError:
            return abort(404)
        codemaker_score, codebreaker_score = game.score()
        return {
            'message': f'This game was created on {game.created}',
            'token': token,
            'score': {
                'codemaker': codemaker_score,
                'codebreaker': codebreaker_score
            }
        }

    def delete(self, token=None):
        """ Delete a game but don't return any content.
        """
        try:
            repo.remove(token)
        except KeyError:
            return abort(404)
        return '', 204

# Endpoint
api.add_resource(Mastermind, '/game/', '/game/<token>')

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')