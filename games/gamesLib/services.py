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
        'hyperlink': game.website_url,
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

def filter_games(batch_of_games, search_term, search_category):
    if search_term is None:
        return batch_of_games
    def filter_fn(game):
        if search_category == 'genre':
            genre_names = map(lambda x: x.genre_name, game['genres'])
            if search_term.title() in genre_names:
                return True
        if search_category == 'title' and search_term.lower() in game['title'].lower():
            return True
        if search_category == 'publisher' and search_term.lower() in game['publisher'].publisher_name.lower():
            return True
        return False
    return list(filter(filter_fn, batch_of_games))


def filter_games_by_genre(batch_of_games, target_genre):
    def filter_by_genre(game):
        genre_names = list(map(lambda x: x.genre_name, game['genres']))
        if target_genre in genre_names:
            return True
        return False

    return list(filter(filter_by_genre, batch_of_games))  # Return games from Game Dictionary based on Genres

# The filter function takes a function and iterables. It will iterate through each item in the dictionary and parse
# the item into the function if filter function return true, we can keep the item, f
