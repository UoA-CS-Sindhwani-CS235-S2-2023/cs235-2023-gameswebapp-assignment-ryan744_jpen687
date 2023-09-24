from games.gameDescription.services import toggle_favourite_game_for_user, is_favourite_game, \
    display_all_reviews_for_a_game, adding_a_new_review_for_game, average_rating_for_a_game


def test_add_favourite_game_for_user(in_memory_repo):
    game = in_memory_repo.get_game(1)
    toggle_favourite_game_for_user(1, "jason", in_memory_repo)
    favourite_games = in_memory_repo.get_users_favourite_games("jason")
    assert favourite_games == [game]


def test_remove_favourite_game_for_user(in_memory_repo):
    in_memory_repo.add_users_favourite_game("jason", 1)
    toggle_favourite_game_for_user(1, "jason", in_memory_repo)
    favourite_games = in_memory_repo.get_users_favourite_games("jason")
    assert favourite_games == []


def test_is_users_favourite_game(in_memory_repo):
    game = in_memory_repo.get_game(1)
    in_memory_repo.add_users_favourite_game("jason", 1)
    favourite_game = is_favourite_game(game, "jason", in_memory_repo)
    assert favourite_game == True


def test_is_not_users_favourite_game(in_memory_repo):
    game = in_memory_repo.get_game(1)
    favourite_game = is_favourite_game(game, "jason", in_memory_repo)
    assert favourite_game == False


def test_add_new_review_on_page_and_displayed_correctly(in_memory_repo):
    adding_a_new_review_for_game(1304320, "ray", 5, "great game released", in_memory_repo)
    adding_a_new_review_for_game(1304320, "jason", 1, "could have been better", in_memory_repo)
    adding_a_new_review_for_game(418650, "jason", 5, "best game, would recommend", in_memory_repo)

    assert len(display_all_reviews_for_a_game(1304320, in_memory_repo)) == 2  # two diff reviews for this game
    assert len(display_all_reviews_for_a_game(1, in_memory_repo)) == 0  # no review for this game
    assert len(display_all_reviews_for_a_game(418650, in_memory_repo)) == 1  # one review for this game


def test_average_rating_displayed_correctly(in_memory_repo):
    adding_a_new_review_for_game(1304320, "ray", 5, "great game released", in_memory_repo)
    adding_a_new_review_for_game(1304320, "jason", 1, "could have been better", in_memory_repo)
    adding_a_new_review_for_game(1304320, "jason", 5, "best game, would recommend", in_memory_repo)
    adding_a_new_review_for_game(1, "jason", 5, "best game, would recommend", in_memory_repo)

    assert average_rating_for_a_game(1304320, in_memory_repo) == 3 # test that only the correct ratings are collected from repo
