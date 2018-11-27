from flask import Flask, request
from flask_restful import Resource, Api, abort

app = Flask(__name__)
api = Api(app)

class Game(Resource):
    def get(self):
        """ Creates a new game
        """
        return {
            'message': 'A new game has been created. Good luck!'
        }

class Guess(Resource):
    def put(self):
        """ Returns feedback given a code pattern guess
        """
        code = request.form.get('code')
        if code is None:
            return abort(400)
        return {
            'message': f'You guessed: {code}',
            'feedback': []
        }

# Endpoints
api.add_resource(Game, '/create/')
api.add_resource(Guess, '/guess/')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')