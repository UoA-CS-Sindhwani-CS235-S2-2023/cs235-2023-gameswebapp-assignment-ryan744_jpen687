"""Initialize Flask app."""

from pathlib import Path

from flask import Flask, render_template

import games.adapters.repository as repo
from games.adapters.memory_repository import MemoryRepository, populate


def create_app():
    app = Flask(__name__)

    repo.repo_instance = MemoryRepository()
    populate(Path('games/adapters/data/games.csv'), repo.repo_instance)

    # TODO: Create this route via blueprint




    with app.app_context():
        from .home import home
        app.register_blueprint(home.home_blueprint)

        from .gamesLib import gamesLib
        app.register_blueprint(gamesLib.gamesLib_blueprint)

        from .utilities import utilities
        app.register_blueprint(utilities.utilities_blueprint)

        from .gameDescription import gameDescription
        app.register_blueprint(gameDescription.gameDescription_blueprint)

    return app

