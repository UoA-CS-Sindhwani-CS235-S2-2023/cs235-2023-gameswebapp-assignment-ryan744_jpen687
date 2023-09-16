import games.adapters.repository as repo
from flask import Blueprint, render_template, request, redirect, url_for, session

import games.utilities.utilities as utilities
import games.gameDescription.services as services
from games.authentication.authentication import login_required, logged_in_username

gameDescription_blueprint = Blueprint(
    'gameDescription_bp', __name__)


@gameDescription_blueprint.route('/game-description/<gameid>', methods=['GET'])
def gameDescription(gameid):
    id = int(gameid)
    active_page = 'gameDescription'
    game = repo.repo_instance.get_game(id)
    if 'username' in session:
      is_favourite_game = services.is_favourite_game(game, session['username'], repo.repo_instance)
    return render_template('gameDescription.html',
      game=game,
      genres=utilities.get_genres(),
      active_page=active_page,
      is_favourite_game=is_favourite_game,
      logged_in_username=logged_in_username(),
    )

@gameDescription_blueprint.route('/toggle-favourite-game', methods=['POST'])
@login_required
def toggleFavouriteGame():
    form_data = request.form
    id = int(form_data['gameId'])
    game = repo.repo_instance.get_game(id)
    services.toggle_favourite_game_for_user(game, session['username'], repo.repo_instance)
    return redirect(url_for('gameDescription_bp.gameDescription', gameid=id))