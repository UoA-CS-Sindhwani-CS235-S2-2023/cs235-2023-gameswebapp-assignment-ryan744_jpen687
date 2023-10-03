from sqlalchemy import select, inspect

from games.adapters.orm import metadata


def test_database_populate_inspect_table_names(database_engine):
    # Get table information
    inspector = inspect(database_engine)
    assert inspector.get_table_names() == ['games', 'genres', 'publishers', 'reviews', 'users','wishlist']


def test_database_populate_select_all_games(database_engine):
    # Get table information
    inspector = inspect(database_engine)
    name_of_games_table = inspector.get_table_names()[0]

    with database_engine.connect() as connection:
        # query for records in table articles
        select_statement = select([metadata.tables[name_of_games_table]])
        result = connection.execute(select_statement)

        all_games = []
        for row in result:
            all_games.append((row['game_id'], row['game_title']))

        nr_games = len(all_games)

        assert nr_games != 8
        assert nr_games == 7

        assert all_games[0] == (1, 'Call of Duty® 4: Modern Warfare®')
        assert all_games[1] == (311120, 'The Stalin Subway: Red Veil')
