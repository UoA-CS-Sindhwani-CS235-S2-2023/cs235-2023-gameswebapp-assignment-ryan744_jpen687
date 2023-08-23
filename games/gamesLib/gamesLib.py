from flask import Blueprint
from flask import request, render_template, redirect, url_for, session
import games.gamesLib.services as services
import games.adapters.repository as repo
from games.utilities import utilities

gamesLib_blueprint = Blueprint(
    'games_bp', __name__)


@gamesLib_blueprint.route('/browse_all_games', methods=['GET'])
def browse_all_games():
    games_per_page = 10
    active_page = browse_all_games

    # Read query parameters.
    cursor = request.args.get('cursor')

    if cursor is None:
        # No cursor query parameter, so initialise cursor to start at the beginning.
        cursor = 0
    else:
        # Convert cursor from string to int.
        cursor = int(cursor)

    batch_of_games = services.get_batch_games(repo.repo_instance)
    length_of_entire_library = len(batch_of_games)

    first_game_url = None
    last_game_url = None
    next_game_url = None
    prev_game_url = None

    if cursor > 0:
        # There are preceding games in the library, generate URL
        first_game_url = url_for('games_bp.browse_all_games', cursor=10)
        prev_game_url = url_for('games_bp.browse_all_games', cursor=cursor - games_per_page)

    if cursor + games_per_page < length_of_entire_library:
        next_game_url = url_for('games_bp.browse_all_games', cursor=cursor + games_per_page)

        last_cursor = length_of_entire_library
        if length_of_entire_library % games_per_page != 0:
            last_cursor -= games_per_page
        last_game_url = url_for('games_bp.browse_all_games', cursor=last_cursor)

    # Retrieve the batch of games to display on the Web page.

    batch_of_games = batch_of_games[cursor:cursor + games_per_page]

    return render_template(
        'library/games.html',
        title='Games',
        batch_of_games=batch_of_games,
        first_game_url=first_game_url,
        last_game_url=last_game_url,
        prev_game_url=prev_game_url,
        next_game_url=next_game_url,
        genres=utilities.get_genres(),
        active_page=active_page
    )
