import pytest

from games.adapters.database_repository import SqlAlchemyRepository
from games.domainmodel.model import Game, Genre, Review, User

def test_repository_can_retrieve_genres(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    genres = repo.get_genres()

    assert len(genres) == 6

def test_repository_can_retrieve_games(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    all_games = repo.get_all_games()

    assert len(all_games) == 7

def test_repository_add_favourite_game(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    repo.add_users_favourite_game('ray', 1)
    favourite_game_ids = repo.get_users_favourite_game_ids('ray')
    assert favourite_game_ids == [1]

def test_repository_remove_favourite_game(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    repo.add_users_favourite_game('ray', 1)
    repo.remove_users_favourite_game('ray', 1)
    favourite_game_ids = repo.get_users_favourite_game_ids('ray')
    assert favourite_game_ids == []