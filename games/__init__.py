"""Initialize Flask app."""

from pathlib import Path

from flask import Flask, render_template

# imports from SQLAlchemy
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker, clear_mappers
from sqlalchemy.pool import NullPool


import games.adapters.repository as repo
from games.adapters import database_repository
from games.adapters.memory_repository import MemoryRepository, populate
from games.adapters.orm import map_model_to_tables, metadata

def create_app(test_config=None):
    app = Flask(__name__)

    # Configure the app from configuration-file settings.
    app.config.from_object('config.Config')
    data_path = Path('games/adapters/data')

    if test_config is not None:
        app.config.from_mapping(test_config)
        data_path = app.config['TEST_DATA_PATH']

    # We can easily switch between in memory data and persistent database data storage for our application.

    if app.config['REPOSITORY'] == 'memory':  # Create the MemoryRepository implementation for a memory-based repository.
        repo.repo_instance = MemoryRepository()
        # fill the content of the repository from the provided csv files (has to be done every time we start app!)
        # database_mode = False
        ### check if the above boolean value needs to be changed for the
        populate(data_path, repo.repo_instance)

    elif app.config['REPOSITORY'] == 'database': # Configure database.
        database_uri = app.config['SQLALCHEMY_DATABASE_URI']

        # We create a comparatively simple SQLite database, which is based on a single file (see .env for URI).
        # For example the file database could be located locally and relative to the application in games.db,
        # leading to a URI of "sqlite:///games.db".
        # Note that create_engine does not establish any actual DB connection directly!
        database_echo = app.config['SQLALCHEMY_ECHO']
        # Please do not change the settings for connect_args and poolclass!
        database_engine = create_engine(database_uri, connect_args={"check_same_thread": False}, poolclass=NullPool,
                                        echo=database_echo)

        # Create the database session factory using sessionmaker (this has to be done once, in a global manner)
        session_factory = sessionmaker(autocommit=False, autoflush=True, bind=database_engine)
        # Create the SQLAlchemy DatabaseRepository instance for an sqlite3-based repository.
        repo.repo_instance = database_repository.SqlAlchemyRepository(session_factory)

        if app.config['TESTING'] == 'True' or len(inspect(database_engine).get_table_names()) == 0:
            print("REPOPULATING DATABASE...")
            # For testing, or first-time use of the web application, reinitialise the database.
            clear_mappers()
            metadata.create_all(database_engine)  # Conditionally create database tables.
            for table in reversed(metadata.sorted_tables):# Remove any data from the tables.
                with database_engine.connect() as conn:
                    conn.execute(table.delete())

            # Generate mappings that map domain model classes to the database tables.
            map_model_to_tables()

            populate(data_path, repo.repo_instance, True)
            print("REPOPULATING DATABASE... FINISHED")

        else:
            # Solely generate mappings that map domain model classes to the database tables.
            map_model_to_tables()


    with app.app_context():
        from .home import home
        app.register_blueprint(home.home_blueprint)

        from .gamesLib import gamesLib
        app.register_blueprint(gamesLib.gamesLib_blueprint)

        from .utilities import utilities
        app.register_blueprint(utilities.utilities_blueprint)

        from .gameDescription import gameDescription
        app.register_blueprint(gameDescription.gameDescription_blueprint)

        from .search import search
        app.register_blueprint(search.search_blueprint)

        from .authentication import authentication
        app.register_blueprint(authentication.authentication_blueprint)

        from .profile import profile
        app.register_blueprint(profile.profile_blueprint)

        # Register a callback the makes sure that database sessions are associated with http requests
        # We reset the session inside the database repository before a new flask request is generated
        @app.before_request
        def before_flask_http_request_function():
            if isinstance(repo.repo_instance, database_repository.SqlAlchemyRepository):
                repo.repo_instance.reset_session()

        # Register a tear-down method that will be called after each request has been processed.
        @app.teardown_appcontext
        def shutdown_session(exception=None):
            if isinstance(repo.repo_instance, database_repository.SqlAlchemyRepository):
                repo.repo_instance.close_session()

    return app
