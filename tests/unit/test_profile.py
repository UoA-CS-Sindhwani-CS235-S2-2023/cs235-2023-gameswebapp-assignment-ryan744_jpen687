from games.gameDescription.services import adding_a_new_review_for_game
from games.profile.services import get_favourite_games, get_reviews_done_by_user
from games.gamesLib.services import multi_games_to_dict
    
def test_add_favourite_game_for_user(in_memory_repo):
    game = in_memory_repo.get_game(1)
    in_memory_repo.add_users_favourite_game("jason", 1)

    favourite_games = get_favourite_games("jason", in_memory_repo)

    assert favourite_games == multi_games_to_dict([game])

def test_show_all_reviews_done_by_user(in_memory_repo):
    adding_a_new_review_for_game(1304320, "jason", 1, "could have been better", in_memory_repo)
    adding_a_new_review_for_game(418650, "jason", 5, "best game, would recommend", in_memory_repo)
    adding_a_new_review_for_game(1228870, "jason", 4, "wonderful game from publisher", in_memory_repo)
    assert len(get_reviews_done_by_user("ray", in_memory_repo)) == 0  # no review done by this user
    assert len(get_reviews_done_by_user("jason", in_memory_repo)) == 3  # 3 reviews were done by this user

