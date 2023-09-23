from games.adapters.memory_repository import MemoryRepository, populate
from games.domainmodel.model import Genre, Game, Publisher, User
from pathlib import Path
import pytest


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
