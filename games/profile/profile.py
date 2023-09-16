from flask import Blueprint, render_template

import games.utilities.utilities as utilities
from games.authentication.authentication import login_required, logged_in_username

profile_blueprint = Blueprint(
    'profile_bp', __name__)


@profile_blueprint.route('/my-profile', methods=['GET'])
@login_required
def profile():
    return render_template(
        'profile/profile.html',
        genres=utilities.get_genres(),
        logged_in_username=logged_in_username(),
      )