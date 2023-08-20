import games.adapters.repository as repo
from flask import Blueprint, render_template

import games.utilities.utilities as utilities

gameDescription_blueprint = Blueprint(
    'gameDescription_bp', __name__)


@gameDescription_blueprint.route('/game-description/<gameid>', methods=['GET'])
def gameDescription(gameid):
    id = int(gameid)
    return render_template('gameDescription.html', game=repo.repo_instance.get_game(id), genres=utilities.get_genres())
