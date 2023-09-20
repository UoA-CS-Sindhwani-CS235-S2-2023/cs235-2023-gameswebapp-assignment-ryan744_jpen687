from games.adapters.repository import AbstractRepository
from games.domainmodel.model import Review


def toggle_favourite_game_for_user(game_id, username, repo: AbstractRepository):
    game = repo.get_game(game_id)
    favourite_games = repo.get_users_favourite_games(username)
    if game in favourite_games:
        repo.remove_users_favourite_game(username, game_id)
    else:
        repo.add_users_favourite_game(username, game_id)


def is_favourite_game(game, username, repo: AbstractRepository):
    favourite_games = repo.get_users_favourite_games(username)
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
        user.add_review(new_review)  # linking the user object to the reivew object
