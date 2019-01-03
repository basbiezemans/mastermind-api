from uuid import uuid4

class GameRepository:
    def __init__(self, builder, gateway):
        self.builder = builder
        self.gateway = gateway

    def save(self, game):
        """ Save and return a Game object
        """
        if hasattr(game, 'token'):
            self.gateway.update(game)
        else:
            game.token = str(uuid4())
            self.gateway.insert(game)
        return game

    def exists(self, token):
        """ Return True if the token exists and False otherwise. 
        """
        return self.gateway.filter_by(token=token) is not None

    def find(self, token):
        """ Return a Game object or raise a KeyError.
        """
        data = self.gateway.filter_by(token=token)
        if data is not None:
            return self.builder \
                .set_token(data['token']) \
                .set_timestamp(data['datetime_created']) \
                .set_codemaker_score(data['codemaker_score']) \
                .set_codebreaker_score(data['codebreaker_score']) \
                .get_result()
        else:
            raise KeyError

    def delete(self, token):
        """ Delete a Game object or raise a KeyError.
        """
        if not self.gateway.delete(token):
            raise KeyError
