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

    # Read query parameters.
    page = request.args.get('page')

    if page is None:
        # No page query parameter, so initialise page to start at the beginning.
        page = 1

    page = int(page)

    batch_of_games = services.get_batch_games(repo.repo_instance)
    length_of_entire_library = len(batch_of_games)

    first_game_url = None
    last_game_url = None
    next_game_url = None
    prev_game_url = None

    if page > 1:
        # There are preceding games in the library, generate URL
        first_game_url = url_for('games_bp.browse_all_games', page=1)
        prev_game_url = url_for('games_bp.browse_all_games', page=page - 1)

    if ((page * games_per_page) + games_per_page) < length_of_entire_library:
        next_game_url = url_for('games_bp.browse_all_games', page=page + 1)
        last_page = int(length_of_entire_library / games_per_page)
        last_game_url = url_for('games_bp.browse_all_games', page=last_page)

    # Retrieve the batch of games to display on the Web page.
    batch_of_games = batch_of_games[(page - 1) * games_per_page: page * games_per_page]

    return render_template(
        'library/games.html',
        title='Games',
        batch_of_games=batch_of_games,
        first_game_url=first_game_url,
        last_game_url=last_game_url,
        prev_game_url=prev_game_url,
        next_game_url=next_game_url,
        genres=utilities.get_genres(),
    )
