from unittest import TestCase
from app.mastermind import *
from app.gateways import SQLiteDatabase
from app.repositories import GameRepository

class TestRepositories(TestCase):

    def test_game_repository(self):
        repo = GameRepository(GameBuilder(), SQLiteDatabase())
        game = Game.create()
        game = repo.save(game)
        self.assertTrue(repo.exists(game.token))
        self.assertEqual(repo.find(game.token), game)
        repo.delete(game.token)
        self.assertFalse(repo.exists(game.token))
