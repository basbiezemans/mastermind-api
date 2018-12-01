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
        guess = codebreaker.guess(request.form.get('code'))
        try:
            feedback = codemaker.feedback(guess)
            game.process(feedback)
            return {
                'message': f'You guessed: {guess.code}',
                'feedback': feedback.response
            }
        except ValueError:
            return abort(400)

# Endpoints
api.add_resource(Create, '/create/')
api.add_resource(Guess, '/guess/')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')