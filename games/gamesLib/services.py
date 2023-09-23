from collections.abc import Iterable

from games.domainmodel.model import Game
from games.adapters.repository import AbstractRepository


def game_to_dict(game: Game):
    # Convert one game to dictionary form.
    summary = ''
    if game.description is not None:
        summary = game.description[:200] + (game.description[200:] and '...')
    game_dict = {
        'id': game.game_id,
        'date': game.release_date,
        'title': game.title,
        'price': game.price,
        'publisher': game.publisher,
        'summary': summary,
        'image_hyperlink': game.image_url,
        'genres': game.genres,
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


def search_games_by_category(search_term, search_category, repo):
    if search_category == 'genre':
        batch_of_games = repo.search_games_by_genre(search_term);
    elif search_category == 'title':
        batch_of_games = repo.search_games_by_title(search_term);
    elif search_category == 'publisher':
        batch_of_games = repo.search_games_by_publisher(search_term);
    return multi_games_to_dict(batch_of_games);

def get_games_by_genre(genre_name, repo):
    return multi_games_to_dict(repo.search_games_by_genre(genre_name));