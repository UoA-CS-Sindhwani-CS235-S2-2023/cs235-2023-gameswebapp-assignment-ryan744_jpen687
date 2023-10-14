import pytest

from games.adapters.database_repository import SqlAlchemyRepository
from games.domainmodel.model import Game, Genre, Review, User, Publisher


def test_repository_can_retrieve_genres(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    genres = repo.get_genres()

    assert len(genres) == 6

def test_repository_can_retrieve_games(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    all_games = repo.get_all_games()

    assert len(all_games) == 7

def test_repository_add_favourite_game(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    repo.add_users_favourite_game('ray', 1)
    favourite_game_ids = repo.get_users_favourite_game_ids('ray')
    assert favourite_game_ids == [1]

def test_repository_remove_favourite_game(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    repo.add_users_favourite_game('ray', 1)
    repo.remove_users_favourite_game('ray', 1)
    favourite_game_ids = repo.get_users_favourite_game_ids('ray')
    assert favourite_game_ids == []

def test_repository_add_reviews(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    user1 = User("jasonp", "JasonP123!")
    user2 = User("username2", "password2")
    game = Game(311120, "The Stalin Subway: Red Veil")
    review1 = Review(user1, game, 3, "Decent")
    review2 = Review(user2, game, 5, "Loved it")
    repo.add_review(review1)
    repo.add_review(review2)
    retrieved_reviews = repo.get_reviews(game)
    assert len(retrieved_reviews) == 2
    assert review1 in retrieved_reviews
    assert review2 in retrieved_reviews

def test_repository_get_reviews(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    user = User("kjwdnaoidnaowdn", "JasonP123!")
    game = Game(311120, "The Stalin Subway: Red Veil")
    review1 = Review(user, game, 2, "Can use improvement")
    repo.add_review(review1)
    retrieved_reviews = repo.get_reviews(game)
    assert len(retrieved_reviews) == 1
    assert review1 in retrieved_reviews

def test_repository_add_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    username = "jasonp"
    password = "JasonP123!"
    user = User(username, password)
    repo.add_user(user)
    retrieved_user = repo.get_user(username)
    assert retrieved_user == user

def test_repository_get_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    username = "jasonp"
    password = "JasonP123!"
    user = User(username, password)
    repo.add_user(user)
    retrieved_user = repo.get_user(username)
    assert retrieved_user == user

def test_repository_add_genre(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    genre_name = "Fun"
    genre = Genre(genre_name)
    repo.add_genre(genre)
    retrieved_genres = repo.get_genres()
    assert genre in retrieved_genres

def test_repository_get_genres(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    genre_name = "Not Fun"
    genre = Genre(genre_name)
    repo.add_genre(genre)
    retrieved_genres = repo.get_genres()
    assert genre in retrieved_genres

def test_repository_add_publisher(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    publisher_name = "Buka Entertainment"
    publisher = Publisher(publisher_name)
    repo.add_publisher(publisher)
    retrieved_publishers = repo.get_publishers()
    assert publisher in retrieved_publishers

def test_repository_get_publishers(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    publisher1 = Publisher("Buka Entertainment")
    publisher2 = Publisher("Activision")
    repo.add_publisher(publisher1)
    repo.add_publisher(publisher2)
    retrieved_publishers = repo.get_publishers()
    assert publisher1 in retrieved_publishers
    assert publisher2 in retrieved_publishers

def test_repository_add_game(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    game = Game(10, "Gamesss")
    repo.add_game(game)
    retrieved_game = repo.get_game(10)
    assert retrieved_game == game

def test_repository_search_games_by_genre(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    retrieved_games = repo.search_games_by_genre('Indie')
    assert retrieved_games == [Game(435790, '10 Second Ninja X'), Game(1304320, '重装无限·Metal Infinite')]

def test_repository_search_games_by_genre_case_insensitive(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    retrieved_games = repo.search_games_by_genre('iNdIe')
    assert retrieved_games == [Game(435790, '10 Second Ninja X'), Game(1304320, '重装无限·Metal Infinite')]

def test_repository_search_games_by_genre_none_found(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    retrieved_games = repo.search_games_by_genre('Fun')
    assert retrieved_games == []

def test_repository_search_games_by_title(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    retrieved_games = repo.search_games_by_title('Ninja')
    assert retrieved_games == [Game(435790, '10 Second Ninja X')]

def test_repository_search_games_by_title_case_insensitive(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    retrieved_games = repo.search_games_by_title('NiNjA')
    assert retrieved_games == [Game(435790, '10 Second Ninja X')]

def test_repository_search_games_by_title_none_found(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    retrieved_games = repo.search_games_by_title('Fun')
    assert retrieved_games == []

def test_repository_search_games_by_publisher(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    retrieved_games = repo.search_games_by_publisher('Activision')
    assert retrieved_games == [Game(1, 'Call of Duty® 4: Modern Warfare®')]

def test_repository_search_games_by_publisher_case_insensitive(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    retrieved_games = repo.search_games_by_publisher('aCtIvIsIoN')
    assert retrieved_games == [Game(1, 'Call of Duty® 4: Modern Warfare®')]

def test_repository_search_games_by_publisher_none_found(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    retrieved_games = repo.search_games_by_publisher('Fun')
    assert retrieved_games == []