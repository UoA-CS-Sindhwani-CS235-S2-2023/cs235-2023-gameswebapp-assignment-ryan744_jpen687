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
    active_page = 'browse_all_games'

    # Read query parameters.
    page = request.args.get('page')
    search_term = request.args.get('search_term')
    search_category = request.args.get('search_category')

    if page is None:
        # No page query parameter, so initialise page to start at the beginning.
        page = 1

    page = int(page)

    batch_of_games = services.get_batch_games(repo.repo_instance)
    batch_of_games = services.filter_games(batch_of_games, search_term, search_category)
    length_of_entire_library = len(batch_of_games)

    first_game_url = None
    last_game_url = None
    next_game_url = None
    prev_game_url = None
    last_page = int(length_of_entire_library / games_per_page + 1)

    if page > 1:
        # There are preceding games in the library, generate URL
        first_game_url = url_for('games_bp.browse_all_games', page=1, search_term=search_term,
                                 search_category=search_category)
        prev_game_url = url_for('games_bp.browse_all_games', page=page - 1, search_term=search_term,
                                search_category=search_category)

    if page < last_page:
        next_game_url = url_for('games_bp.browse_all_games', page=page + 1, search_term=search_term,
                                search_category=search_category)
        last_game_url = url_for('games_bp.browse_all_games', page=last_page, search_term=search_term,
                                search_category=search_category)

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
        page=page,
        last_page=last_page,
        active_page = active_page
    )


@gamesLib_blueprint.route('/browse_games_by_genre', methods=['GET'])
def browse_games_by_genre():
    games_per_page = 10


    # Read query parameters.
    page = request.args.get('page')
    target_genre = request.args.get('genre')
    active_page = 'browse_games_by_genre_' + target_genre

    if page is None:
        # No page query parameter, so initialise page to start at the beginning.
        page = 1

    page = int(page)

    batch_of_games = services.get_batch_games(repo.repo_instance) #get whole repo
    batch_of_games = services.filter_games_by_genre(batch_of_games, target_genre)
    length_of_entire_glibrary = len(batch_of_games)

    first_game_url = None
    last_game_url = None
    next_game_url = None
    prev_game_url = None
    last_page = int(length_of_entire_glibrary / games_per_page + 1)

    if page > 1:
        # There are preceding games in the library, generate URL
        first_game_url = url_for('games_bp.browse_games_by_genre', page=1)
        prev_game_url = url_for('games_bp.browse_games_by_genre', page=page - 1, )

    if page < last_page:
        next_game_url = url_for('games_bp.browse_games_by_genre', page=page + 1,)
        last_game_url = url_for('games_bp.browse_games_by_genre', page=last_page,)

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
        page=page,
        last_page=last_page,
        active_page=active_page
    )

