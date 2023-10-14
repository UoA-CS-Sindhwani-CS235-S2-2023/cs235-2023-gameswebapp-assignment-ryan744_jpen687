import pytest

from sqlalchemy.exc import IntegrityError

from games.domainmodel.model import Game, Genre, Review, User, Publisher

def insert_user(empty_session, values=None):
    new_name = "Andrew"
    new_password = "1234"

    if values is not None:
        new_name = values[0]
        new_password = values[1]

    empty_session.execute('INSERT INTO users (username, password) VALUES (:username, :password)',
                          {'username': new_name, 'password': new_password})
    row = empty_session.execute('SELECT username from users where username = :username',
                                {'username': new_name}).fetchone()
    return row[0]

def insert_users(empty_session, values):
    for value in values:
        empty_session.execute('INSERT INTO users (username, password) VALUES (:username, :password)',
                              {'username': value[0], 'password': value[1]})
    rows = list(empty_session.execute('SELECT username from users'))
    keys = tuple(row[0] for row in rows)
    return keys

def insert_game(empty_session):
    empty_session.execute(
        'INSERT INTO games (game_id, game_title, game_price, release_date) VALUES '
        '(1, "Game", 100, "Oct 21, 2008")'
    )
    row = empty_session.execute('SELECT game_id from games').fetchone()
    return row[0]

def insert_genres(empty_session):
    empty_session.execute(
        'INSERT INTO genres (genre_name) VALUES ("Action"), ("Adventure")'
    )
    rows = list(empty_session.execute('SELECT genre_name from genres'))
    keys = tuple(row[0] for row in rows)
    return keys

def insert_game_genre_associations(empty_session, game_id, genre_names):
    stmt = 'INSERT INTO game_genres (game_id, genre_name) VALUES (:game_id, :genre_name)'
    for genre_name in genre_names:
        empty_session.execute(stmt, {'game_id': game_id, 'genre_name': genre_name})

def insert_reviewed_game(empty_session):
    game_id = insert_game(empty_session)
    user_id = insert_user(empty_session)

    empty_session.execute(
        'INSERT INTO reviews (review_id, review_comment, review_rating, user_id, game_id) VALUES '
        '(1, "Good Game", 5, :user_id, :game_id),'
        '(2, "Bad Game", 1, :user_id, :game_id)',
        {'user_id': user_id, 'game_id': game_id}
    )

    row = empty_session.execute('SELECT review_id from reviews').fetchone()
    return row[0]


def make_user():
    user = User("andrew", "aA123456")
    return user

def make_game():
    game = Game(
        1,
        "Game"
    )
    game.price = 100
    game.release_date = 'Oct 21, 2008'
    return game

def test_loading_of_users(empty_session):
    users = list()
    users.append(("andrew", "1234abcd"))
    users.append(("cindy", "baiwdnaidw1234fa2"))
    insert_users(empty_session, users)

    expected = [
        User("andrew", "1234abcd"),
        User("cindy", "baiwdnaidw1234fa2")
    ]
    assert empty_session.query(User).all() == expected

def test_saving_of_users(empty_session):
    user = make_user()
    empty_session.add(user)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT username, password FROM users'))
    assert rows == [("andrew", "aA123456")]

def test_saving_of_users_with_common_user_name(empty_session):
    insert_user(empty_session, ("andrew", "aA123456"))
    empty_session.commit()

    with pytest.raises(IntegrityError):
        user = User("andrew", "aA123456")
        empty_session.add(user)
        empty_session.commit()

def test_loading_of_games(empty_session):
    game_id = insert_game(empty_session)
    expected_game = make_game()
    fetched_game = empty_session.query(Game).one()

    assert expected_game == fetched_game
    assert game_id == fetched_game.game_id

def test_loading_of_games_with_genres(empty_session):
    game_id = insert_game(empty_session)
    genre_names = insert_genres(empty_session)
    insert_game_genre_associations(empty_session, game_id, genre_names)

    game = empty_session.query(Game).get(game_id)
    genres = [empty_session.query(Genre).get(genre_name) for genre_name in genre_names]

    for genre in genres:
      assert genre in game.genres

def test_loading_of_reviewed_game(empty_session):
    insert_reviewed_game(empty_session)

    rows = empty_session.query(Review).all()
    review = rows[0]

    rows = empty_session.query(Game).all()
    game = rows[0]

    assert review.game is game

def test_saving_of_review(empty_session):
    game_id = insert_game(empty_session)
    insert_user(empty_session, ("andrew", "abadasd12134faAA"))

    rows = empty_session.query(Game).all()
    game = rows[0]
    user = empty_session.query(User).filter(User._User__username == "andrew").one()

    # Create a new Review that is bidirectionally linked with the User and Game.
    review = Review(user, game, 5, "Good Game")
    user.add_review(review)

    empty_session.add(review)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT user_id, game_id, review_comment FROM reviews'))

    assert rows == [(1, game_id, "Good Game")]

def test_saving_of_game(empty_session):
    game = make_game()
    empty_session.add(game)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT game_id, game_title, game_price, release_date FROM games'))
    assert rows == [(1, "Game", 100, "Oct 21, 2008")]

def test_saving_game_with_genre(empty_session):
    game = make_game()
    genre = Genre("Action")

    # Establish the bidirectional relationship between the Game and the Genre.
    game.add_genre(genre)

    empty_session.add(game)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT game_id FROM games'))
    game_id = rows[0][0]

    # Check that the genres table has a new record.
    rows = list(empty_session.execute('SELECT genre_name FROM genres'))
    genre_name = rows[0][0]
    assert genre_name == "Action"

    # Check that the games_genres table has a new record.
    rows = list(empty_session.execute('SELECT game_id, genre_name from game_genres'))
    game_id_fk = rows[0][0]
    genre_name_fk = rows[0][1]

    assert game_id == game_id_fk
    assert genre_name == genre_name_fk

def test_save_reviewed_game(empty_session):
    game = make_game()
    user = make_user()

    # Create a new Review that is bidirectionally linked with the User and Game.
    review = Review(user, game, 5, "Good Game")
    user.add_review(review)

    # Save the new Article.
    empty_session.add(game)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT game_id FROM games'))
    game_id = rows[0][0]

    rows = list(empty_session.execute('SELECT user_id FROM users'))
    user_id = rows[0][0]

    # Check that the reviews table has a new record that links to the games and users
    # tables.
    rows = list(empty_session.execute('SELECT user_id, game_id, review_comment FROM reviews'))
    assert rows == [(user_id, game_id, "Good Game")]