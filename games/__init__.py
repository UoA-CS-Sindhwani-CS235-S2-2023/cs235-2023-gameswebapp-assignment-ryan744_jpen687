"""Initialize Flask app."""

from pathlib import Path

from flask import Flask, render_template

import games.adapters.repository as repo
from games.adapters.memory_repository import MemoryRepository, populate

def create_app():
    """Construct the core application."""

    # Create the Flask app object.
    app = Flask(__name__)

    repo.repo_instance = MemoryRepository()
    populate(Path('games/adapters/data/games.csv'), repo.repo_instance)

    # TODO: Create this route via blueprint
    @app.route('/')
    def home():
        # Use Jinja to customize a predefined html page rendering the layout for showing a single game.
        CALL_OF_DUTY_GAME_ID = 7940
        return render_template('gameDescription.html', game=repo.repo_instance.get_game(CALL_OF_DUTY_GAME_ID))

    return app
