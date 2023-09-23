from games.gameDescription.services import toggle_favourite_game_for_user, is_favourite_game
from games.adapters import memory_repository
from games.adapters.memory_repository import MemoryRepository
from games.domainmodel.model import User
from pathlib import Path
import pytest

TEST_DATA_PATH = Path('tests/data')

class TestGameDescription:
    @pytest.fixture
    def mock_repo(self):
        repo = MemoryRepository()
        memory_repository.populate(TEST_DATA_PATH, repo)
        user = User("User", "Aa123456")
        repo.add_user(user)
        return repo
    
    def test_add_favourite_game_for_user(self, mock_repo):
        game = mock_repo.get_game(1)
        toggle_favourite_game_for_user(1, "User", mock_repo)
        favourite_games = mock_repo.get_users_favourite_games("User")
        assert favourite_games == [game]

    def test_remove_favourite_game_for_user(self, mock_repo):
        mock_repo.add_users_favourite_game("User", 1)
        toggle_favourite_game_for_user(1, "User", mock_repo)
        favourite_games = mock_repo.get_users_favourite_games("User")
        assert favourite_games == []

    def test_is_users_favourite_game(self, mock_repo):
        game = mock_repo.get_game(1)
        mock_repo.add_users_favourite_game("User", 1)
        favourite_game = is_favourite_game(game, "User", mock_repo)
        assert favourite_game == True

    def test_is_not_users_favourite_game(self, mock_repo):
        game = mock_repo.get_game(1)
        favourite_game = is_favourite_game(game, "User", mock_repo)
        assert favourite_game == False


