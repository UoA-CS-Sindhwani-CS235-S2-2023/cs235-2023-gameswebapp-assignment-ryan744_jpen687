from games.profile.services import get_favourite_games
from games.gamesLib.services import multi_games_to_dict
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
        mock_repo.add_users_favourite_game("User", 1)

        favourite_games = get_favourite_games("User", mock_repo)

        assert favourite_games == multi_games_to_dict([game])


