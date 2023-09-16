from flask import Blueprint, render_template, session

import games.utilities.utilities as utilities
import games.profile.services as services
import games.adapters.repository as repo
from games.authentication.authentication import login_required, logged_in_username

profile_blueprint = Blueprint(
    'profile_bp', __name__)


@profile_blueprint.route('/my-profile', methods=['GET'])
@login_required
def profile():
    favourite_games = services.get_favourite_games(session['username'], repo.repo_instance)
    all_reviewed_games_by_user = services.get_reviews_done_by_user(session['username'], repo.repo_instance)
    return render_template(
        'profile/profile.html',
        genres=utilities.get_genres(),
        logged_in_username=logged_in_username(),
        favourite_games=favourite_games,
        reviews=all_reviewed_games_by_user,
    )
