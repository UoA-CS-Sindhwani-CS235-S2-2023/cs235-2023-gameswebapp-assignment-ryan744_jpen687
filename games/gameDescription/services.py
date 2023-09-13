from games.adapters.repository import AbstractRepository

def toggle_favourite_game_for_user(game, username, repo: AbstractRepository):
    user = repo.get_user(username)
    if(game in user.favourite_games):
        user.remove_favourite_game(game)
    else:
        user.add_favourite_game(game)

def is_favourite_game(game, username, repo: AbstractRepository):
    if username is None:
        return False;
    user = repo.get_user(username)
    if user is None:
        return False;
    favourite_games = user.favourite_games;
    if(game in favourite_games):
        return True
    else:
        return False
