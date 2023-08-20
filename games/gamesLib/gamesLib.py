from flask import Blueprint
from flask import request, render_template, redirect, url_for, session
import games.gamesLib.services as services
import games.adapters.repository as repo

gamesLib_blueprint = Blueprint(
    'games_bp', __name__)


@gamesLib_blueprint.route('/browse_all_games', methods=['POST', 'GET'])
def browse_all_games():
    games_per_page = 10

    # Read query parameters.
    cursor = request.args.get('cursor')

    if cursor is None:
        # No cursor query parameter, so initialise cursor to start at the beginning.
        cursor = 0
    else:
        # Convert cursor from string to int.
        cursor = int(cursor)

    # Retrieve games
    # games_ids = services.get_batch_games(repo.repo_instance)

    # Retrieve the batch of games to display on the Web page.
    batch_of_games = services.get_batch_games(repo.repo_instance)

    batch_of_games = batch_of_games[cursor:cursor + games_per_page]

    first_game_url = None
    last_game_url = None
    next_game_url = None
    prev_game_url = None

    if cursor >= 0:
        prev_game_url = url_for('games_bp.browse_all_games', cursor=cursor - games_per_page)
        first_game_url = url_for('games_bp.browse_all_games', cursor=10)
        next_game_url = url_for('games_bp.browse_all_games', cursor=cursor + games_per_page)
        last_game_url = url_for('games_bp.browse_all_games', cursor=len(batch_of_games) - games_per_page)

    return render_template(
        'library/games.html',
        title='Games',
        batch_of_games=batch_of_games,
        first_game_url=first_game_url,
        last_game_url=last_game_url,
        prev_game_url=prev_game_url,
        next_game_url=next_game_url,
    )
