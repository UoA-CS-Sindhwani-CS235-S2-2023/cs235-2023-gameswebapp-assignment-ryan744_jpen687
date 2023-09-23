from games.adapters.memory_repository import MemoryRepository, populate
from games.domainmodel.model import Genre, Game, Publisher, User
from pathlib import Path
import pytest

class TestMemoryRepository:
    @pytest.fixture
    def empty_repository(self):
        return MemoryRepository()

    def test_add_publisher(self, empty_repository):
        publisher = Publisher("Publisher A")
        empty_repository.add_publisher(publisher)
        publishers = empty_repository.get_publishers()
        assert publisher in publishers

    def test_add_genre(self, empty_repository):
        genre = Genre("Genre X")
        empty_repository.add_genre(genre)
        genres = empty_repository.get_genres()
        assert genre in genres

    def test_add_game(self, empty_repository):
        game = Game(1, "Game A")
        empty_repository.add_game(game)
        added_game = empty_repository.get_game(1)
        assert added_game == game

    def test_get_game_nonexistent(self, empty_repository):
        non_existent_game = empty_repository.get_game(999)
        assert non_existent_game is None

    def test_populate(self, empty_repository):
        data_path = Path('tests/data')
        populate(data_path, empty_repository)
        assert empty_repository.get_game(1) is not None
        assert len(empty_repository.get_publishers()) > 0
        assert len(empty_repository.get_genres()) > 0
    
    def test_add_duplicate_publisher(self, empty_repository):
        publisher = Publisher("Publisher A")
        empty_repository.add_publisher(publisher)
        empty_repository.add_publisher(publisher)
        assert len(empty_repository.get_publishers()) == 1
    
    def test_add_duplicate_genre(self, empty_repository):
        genre = Genre("Genre X")
        empty_repository.add_genre(genre)
        empty_repository.add_genre(genre)
        assert len(empty_repository.get_genres()) == 1

    def test_add_users_favourite_game(self, empty_repository):
        game = Game(1, "Game A")
        empty_repository.add_game(game)
        user = User("Ray", "aA123456")
        empty_repository.add_user(user)
        
        empty_repository.add_users_favourite_game("Ray", 1)

        favourite_games = empty_repository.get_users_favourite_games("Ray")
        assert favourite_games == [game]

    def test_remove_users_favourite_game(self, empty_repository):
        game = Game(1, "Game A")
        empty_repository.add_game(game)
        user = User("Ray", "aA123456")
        empty_repository.add_user(user)
        empty_repository.add_users_favourite_game("Ray", 1)

        empty_repository.remove_users_favourite_game("Ray", 1)

        favourite_games = empty_repository.get_users_favourite_games("Ray")
        assert favourite_games == []
