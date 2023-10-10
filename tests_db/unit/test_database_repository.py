import pytest

from games.adapters.database_repository import SqlAlchemyRepository
from games.domainmodel.model import Game, Genre, Review, User

def test_repository_can_retrieve_tags(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    genres = repo.get_genres()

    assert len(genres) == 6

def test_repository_can_retrieve_games(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    all_games = repo.get_all_games()

    assert len(all_games) == 7