from flask import Flask, request
from flask_restful import Resource, Api, abort
from mastermind import Game, CodeMaker, CodeBreaker

app = Flask(__name__)
api = Api(app)

codemaker = CodeMaker()
codebreaker = CodeBreaker()

game = Game(codemaker, codebreaker)

class Create(Resource):
    def get(self):
        """ Creates a new game
        """
        game.create()
        return {
            'message': 'A new game has been created. Good luck!',
            'guesses': game.turns
        }, 201

class Guess(Resource):
    def put(self):
        """ Returns feedback given a code pattern guess
        """
        if not game.ready:
            return {
                'message': 'You first have to create a game.',
                'feedback': []
            }, 403
        guess = codebreaker.guess(request.form.get('code'))
        try:
            feedback = codemaker.feedback(guess)
        except ValueError:
            return abort(400)
        else:
            game.process(feedback)
            if feedback.result.is_correct() or game.has_no_turns_left():
                result = 'CORRECT!' if feedback.result.is_correct() else 'Game Over!'
                message = (
                    f'{result} The current score is '
                    f'{codebreaker.points} (You) vs {codemaker.points} (CodeMaker).'
                )
            else:
                message = (
                    f'Guess {game.turn_counter} of {game.turns}. '
                    f'You guessed: {guess.code}'
                )
            return {
                'message': message,
                'feedback': feedback.response
            }

# Endpoints
api.add_resource(Create, '/create/')
api.add_resource(Guess, '/guess/')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')