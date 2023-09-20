from games.gamesLib.services import multi_games_to_dict


def get_favourite_games(username, repo):
    favourite_games = repo.get_users_favourite_games(username)
    return multi_games_to_dict(favourite_games)


def get_reviews_done_by_user(username, repo):
    user = repo.get_user(username)
    all_reviews_by_this_user = user.reviews #list of reviews
    return all_reviews_by_this_user
