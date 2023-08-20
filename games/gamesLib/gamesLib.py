from flask import Blueprint
from flask import request, render_template, redirect, url_for, session
import games.gamesLib.services as services
import games.adapters.repository as repo

gamesLib_blueprint = Blueprint(
    'games_bp', __name__)


@gamesLib_blueprint.route('/browse_all_games', methods=['GET'])
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

    first_game_url = None
    last_game_url = None
    next_game_url = None
    prev_game_url = None

    # if cursor > 0:
    #     # There are preceding articles, so generate URLs for the 'previous' and 'first' navigation buttons.
    #     prev_game_url = url_for('games_bp.browse_all_games', cursor=cursor - games_per_page)
    #     first_game_url = url_for('games_bp.browse_all_games')
    #
    # if cursor + games_per_page < len(games_ids):
    #     # There are further articles, so generate URLs for the 'next' and 'last' navigation buttons.
    #     next_game_url = url_for('games_bp.browse_all_games', cursor=cursor + games_per_page)
    #
    #     last_cursor = games_per_page * int(len(games_ids) / games_per_page)
    #     if len(games_ids) % games_per_page == 0:
    #         last_cursor -= games_per_page
    #     last_game_url = url_for('games_bp.browse_all_games', cursor=last_cursor)

    return render_template(
        '/games.html',
        title='Games',
        batch_of_games=batch_of_games,
        first_game_url=first_game_url,
        last_game_url=last_game_url,
        prev_game_url=prev_game_url,
        next_game_url=next_game_url,
    )
