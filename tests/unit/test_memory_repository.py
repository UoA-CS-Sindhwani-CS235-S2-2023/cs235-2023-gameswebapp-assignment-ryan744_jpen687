import pytest

from games.adapters.repository import RepositoryException
from games.domainmodel.model import Genre, Game, Publisher, User, Review


def test_add_publisher(in_memory_repo):
    publisher = Publisher("Publisher A")
    in_memory_repo.add_publisher(publisher)
    publishers = in_memory_repo.get_publishers()
    assert publisher in publishers


def test_add_genre(in_memory_repo):
    genre = Genre("Genre X")
    in_memory_repo.add_genre(genre)
    genres = in_memory_repo.get_genres()
    assert genre in genres


def test_add_game(in_memory_repo):
    game = Game(1, "Game A")
    in_memory_repo.add_game(game)
    added_game = in_memory_repo.get_game(1)
    assert added_game == game


def test_get_game_nonexistent(in_memory_repo):
    non_existent_game = in_memory_repo.get_game(999)
    assert non_existent_game is None


def test_add_duplicate_publisher(in_memory_repo):
    publisher = Publisher("Publisher A")
    in_memory_repo.add_publisher(publisher)
    in_memory_repo.add_publisher(publisher)
    assert len(set(in_memory_repo.get_publishers())) == len(in_memory_repo.get_publishers())


def test_add_duplicate_genre(in_memory_repo):
    genre = Genre("Genre X")
    in_memory_repo.add_genre(genre)
    in_memory_repo.add_genre(genre)
    assert len(set(in_memory_repo.get_genres())) == len(in_memory_repo.get_genres())


def test_add_users_favourite_game(in_memory_repo):
    game = Game(1, "Game A")
    in_memory_repo.add_game(game)
    user = User("Xi", "aA123456")
    in_memory_repo.add_user(user)

    in_memory_repo.add_users_favourite_game("Xi", 1)

    favourite_games = in_memory_repo.get_users_favourite_games("Xi")
    assert favourite_games == [game]


def test_remove_users_favourite_game(in_memory_repo):
    game = Game(1, "Game A")
    in_memory_repo.add_game(game)
    user = User("Xi", "aA123456")
    in_memory_repo.add_user(user)
    in_memory_repo.add_users_favourite_game("Xi", 1)

    in_memory_repo.remove_users_favourite_game("Xi", 1)

    favourite_games = in_memory_repo.get_users_favourite_games("Xi")
    assert favourite_games == []


def test_search_games_by_genre(in_memory_repo):
    expected = [Game(435790, '10 Second Ninja X'), Game(1304320, '重装无限·Metal Infinite')]
    games = in_memory_repo.search_games_by_genre('Indie')
    assert games == expected


def test_search_games_by_genre_none_found(in_memory_repo):
    games = in_memory_repo.search_games_by_genre('Lots of Fun')
    assert games == []


def test_search_games_by_genre_case_insensitive(in_memory_repo):
    games = in_memory_repo.search_games_by_genre('Indie')
    assert games == in_memory_repo.search_games_by_genre('indie')
    assert games == in_memory_repo.search_games_by_genre('INDIE')
    assert games == in_memory_repo.search_games_by_genre('InDiE')


def test_search_games_by_title(in_memory_repo):
    expected = [Game(435790, '10 Second Ninja X')]
    games = in_memory_repo.search_games_by_title('Ninja')
    assert games == expected


def test_search_games_by_title_none_found(in_memory_repo):
    games = in_memory_repo.search_games_by_title('Lots of Fun')
    assert games == []


def test_search_games_by_title_case_insensitive(in_memory_repo):
    games = in_memory_repo.search_games_by_title('Ninja')
    assert games == in_memory_repo.search_games_by_title('NINJA')
    assert games == in_memory_repo.search_games_by_title('ninja')
    assert games == in_memory_repo.search_games_by_title('NiNjA')


def test_search_games_by_publisher(in_memory_repo):
    expected = [Game(435790, '10 Second Ninja X')]
    games = in_memory_repo.search_games_by_publisher('Curve Games')
    assert games == expected


def test_search_games_by_publisher_none_found(in_memory_repo):
    games = in_memory_repo.search_games_by_publisher('Lots of Fun')
    assert games == []


def test_search_games_by_publisher_case_insensitive(in_memory_repo):
    games = in_memory_repo.search_games_by_publisher('Curve Games')
    assert games == in_memory_repo.search_games_by_publisher('CURVE GAMES')
    assert games == in_memory_repo.search_games_by_publisher('curve games')
    assert games == in_memory_repo.search_games_by_publisher('CuRvE gAmEs')


def test_repo_can_add_a_comment(in_memory_repo):
    user = in_memory_repo.get_user("ray")
    game_to_review = in_memory_repo.get_game(311120)
    review = Review(user, game_to_review, 4, 'awesome game!')

    in_memory_repo.add_review(review)
    assert review in in_memory_repo.get_reviews()


def test_repo_does_not_add_a_comment_without_a_user(in_memory_repo):
    game_to_review = in_memory_repo.get_game(311120)

    with pytest.raises(ValueError):
        no_user_review = Review(None, game_to_review, 1, 'average game released this year')
        in_memory_repo.add_review(no_user_review)


def test_repo_does_not_add_a_comment_without_a_game_properly_attached(in_memory_repo):
    user = in_memory_repo.get_user("ray")
    game_to_review = in_memory_repo.get_game(445566)  # non - existential game in repo

    with pytest.raises(ValueError):
        no_game_review = Review(user, game_to_review, 3, 'its alright')
        in_memory_repo.add_review(no_game_review)


def test_repo_can_retrieve_reviews(in_memory_repo):
    assert len(in_memory_repo.get_reviews()) == 0
    review_1 = Review(in_memory_repo.get_user("ray"), in_memory_repo.get_game(311120), 4, 'awesome game!')
    review_2 = Review(in_memory_repo.get_user("jason"), in_memory_repo.get_game(311120), 4, 'awesome game!')
    in_memory_repo.add_review(review_1)
    in_memory_repo.add_review(review_2)
    assert len(in_memory_repo.get_reviews()) == 2

