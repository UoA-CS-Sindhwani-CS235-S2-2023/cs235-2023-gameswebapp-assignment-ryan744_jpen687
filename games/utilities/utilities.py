from flask import Blueprint

import games.adapters.repository as repo
import games.utilities.services as services

# Configure Blueprint.
utilities_blueprint = Blueprint(
    'utilities_bp', __name__)


def get_genres():
    genres = services.get_genres(repo.repo_instance)
    if genres is not None:
        return genres
