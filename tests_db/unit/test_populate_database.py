from sqlalchemy import select, inspect

from games.adapters.orm import metadata


def test_database_populate_inspect_table_names(database_engine):
    # Get table information
    inspector = inspect(database_engine)
    assert inspector.get_table_names() == ['favourites', 'game_genres', 'games', 'genres', 'publishers', 'reviews', 'users']


def test_database_populate_select_all_games(database_engine):
    # Get table information
    inspector = inspect(database_engine)
    name_of_games_table = inspector.get_table_names()[2]

    with database_engine.connect() as connection:
        # query for records in table articles
        select_statement = select([metadata.tables[name_of_games_table]])
        result = connection.execute(select_statement)

        all_games = []
        for row in result:
            all_games.append((row['game_id'], row['game_title']))

        nr_games = len(all_games)
        assert nr_games == 7

        assert all_games[0] == (1, 'Call of Duty® 4: Modern Warfare®')
        assert all_games[1] == (311120, 'The Stalin Subway: Red Veil')

def test_database_populate_select_all_genres(database_engine):
    # Get table information
    inspector = inspect(database_engine)
    name_of_genre_table = inspector.get_table_names()[3]

    with database_engine.connect() as connection:
        # query for records in table articles
        select_statement = select([metadata.tables[name_of_genre_table]])
        result = connection.execute(select_statement)

        all_genres = []
        for row in result:
            all_genres.append((row['genre_name']))

        nr_games = len(all_genres)
        assert nr_games == 6

        assert all_genres[0] == ('Action')

def test_database_populate_select_all_games_genres_association(database_engine):
    # Get table information
    inspector = inspect(database_engine)
    name_of_table = inspector.get_table_names()[1]

    with database_engine.connect() as connection:
        # query for records in table articles
        select_statement = select([metadata.tables[name_of_table]])
        result = connection.execute(select_statement)

        all_items = []
        for row in result:
            all_items.append((row['genre_name'], row['game_id']))

        nr_games = len(all_items)
        assert nr_games == 13

        assert all_items[0] == ('Action', 1)

def test_database_populate_select_all_publishers(database_engine):
    # Get table information
    inspector = inspect(database_engine)
    name_of_table = inspector.get_table_names()[4]

    with database_engine.connect() as connection:
        # query for records in table articles
        select_statement = select([metadata.tables[name_of_table]])
        result = connection.execute(select_statement)

        all_items = []
        for row in result:
            all_items.append((row['name']))

        nr_games = len(all_items)
        assert nr_games == 14

        assert all_items[0] == ('Activision')

def test_database_populate_select_all_users(database_engine):
    # Get table information
    inspector = inspect(database_engine)
    name_of_table = inspector.get_table_names()[6]

    with database_engine.connect() as connection:
        # query for records in table articles
        select_statement = select([metadata.tables[name_of_table]])
        result = connection.execute(select_statement)

        all_items = []
        for row in result:
            all_items.append((row['username']))

        nr_games = len(all_items)
        assert nr_games == 2

        assert all_items[0] == ('jason')