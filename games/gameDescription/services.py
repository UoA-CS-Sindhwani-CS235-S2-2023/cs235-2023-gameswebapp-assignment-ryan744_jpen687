from games.adapters.repository import AbstractRepository
from games.domainmodel.model import Review


def toggle_favourite_game_for_user(game, username, repo: AbstractRepository):
    user = repo.get_user(username)
    if game in user.favourite_games:
        user.remove_favourite_game(game)
    else:
        user.add_favourite_game(game)


def is_favourite_game(game, username, repo: AbstractRepository):
    if username is None:
        return False
    user = repo.get_user(username)
    if user is None:
        return False
    favourite_games = user.favourite_games
    if game in favourite_games:
        return True
    else:
        return False


def display_all_reviews_for_a_game(gameID, repo: AbstractRepository):
    if gameID is not None:
        all_reviews = repo.get_game(gameID).reviews
        return all_reviews


def adding_a_new_review_for_game(gameID, username, new_rating, new_comment, repo: AbstractRepository):
    if gameID is not None:
        game = repo.get_game(gameID)
        user = repo.get_user(username)
        new_review = Review(user, game, new_rating, new_comment)
        game.reviews.append(new_review)
