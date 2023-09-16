from flask import Blueprint, render_template

import games.utilities.utilities as utilities
from games.authentication.authentication import logged_in_username

home_blueprint = Blueprint(
    'home_bp', __name__)


@home_blueprint.route('/', methods=['GET'])
def home():
    active_page = 'home'
    return render_template(
        'home/home.html',
        genres=utilities.get_genres(),
        active_page=active_page,
        logged_in_username=logged_in_username(),
      )