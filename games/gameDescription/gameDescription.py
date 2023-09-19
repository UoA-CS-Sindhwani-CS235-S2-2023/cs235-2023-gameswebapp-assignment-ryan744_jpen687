import games.adapters.repository as repo
from flask import Blueprint, render_template, request, redirect, url_for, session

import games.utilities.utilities as utilities
import games.gameDescription.services as services
from games.authentication.authentication import login_required, logged_in_username

gameDescription_blueprint = Blueprint(
    'gameDescription_bp', __name__)


@gameDescription_blueprint.route('/game-description/<gameid>', methods=['GET'])
def gameDescription(gameid, rating=None, comment=None):
    id = int(gameid)
    active_page = 'gameDescription'
    game = repo.repo_instance.get_game(id)
    if 'username' in session:
        is_favourite_game = services.is_favourite_game(game, session['username'], repo.repo_instance)
    else:
        is_favourite_game = False

    reviews_of_this_game = services.display_all_reviews_for_a_game(id, repo.repo_instance)

    return render_template('gameDescription.html',
                           game=game,
                           genres=utilities.get_genres(),
                           active_page=active_page,
                           is_favourite_game=is_favourite_game,
                           logged_in_username=logged_in_username(),
                           all_reviews=reviews_of_this_game,
                           )


@gameDescription_blueprint.route('/toggle-favourite-game', methods=['POST'])
@login_required
def toggleFavouriteGame():
    form_data = request.form
    id = int(form_data['gameId'])
    services.toggle_favourite_game_for_user(id, session['username'], repo.repo_instance)
    return redirect(url_for('gameDescription_bp.gameDescription', gameid=id))


@gameDescription_blueprint.route('/add_review', methods=['GET', 'POST'])
@login_required
def adding_review_for_a_game():
    form_data = request.form
    id = int(form_data['gameId'])
    rating = int(form_data['rating'])
    comment = str(form_data['comment'])
    services.adding_a_new_review_for_game(id, session['username'], rating, comment, repo.repo_instance)
    return redirect(url_for('gameDescription_bp.gameDescription', gameid=id))
