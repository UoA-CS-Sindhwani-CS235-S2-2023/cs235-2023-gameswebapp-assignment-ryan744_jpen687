from games.gameDescription.services import toggle_favourite_game_for_user, is_favourite_game

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


