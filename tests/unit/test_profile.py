from games.profile.services import get_favourite_games
from games.gamesLib.services import multi_games_to_dict
    
def test_add_favourite_game_for_user(in_memory_repo):
    game = in_memory_repo.get_game(1)
    in_memory_repo.add_users_favourite_game("jason", 1)

    favourite_games = get_favourite_games("jason", in_memory_repo)

    assert favourite_games == multi_games_to_dict([game])


