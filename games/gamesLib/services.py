from collections.abc import Iterable

from games.domainmodel.model import Publisher, Genre, Game
from games.adapters.repository import AbstractRepository


def game_to_dict(game: Game):
    # Convert one game to dictionary form.
    game_dict = {
        'id': game.game_id,
        'date': game.release_date,
        'title': game.title,
        'price': game.price,
        'publisher': game.publisher,
        'first_paragraph': game.description,
        'hyperlink': game.website_url,
        'image_hyperlink': game.image_url,
    }
    return game_dict


def multi_games_to_dict(games: Iterable[Game]):
    return [game_to_dict(game) for game in games]


def get_batch_games(repo: AbstractRepository):

    # Return in a list of Games Object
    game_objects_with_id = repo.get_all_games()

    # Convert Games to dictionary form.
    games_as_dict = multi_games_to_dict(game_objects_with_id)

    return games_as_dict


def get_first_article(repo: AbstractRepository):
    game = repo.get_first_game()
    return game_to_dict(game)


def get_last_article(repo: AbstractRepository):
    game = repo.get_last_game()
    return game_to_dict(game)

