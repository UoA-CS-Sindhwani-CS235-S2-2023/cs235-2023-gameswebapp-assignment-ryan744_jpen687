from typing import Iterable
import random

from games.adapters.repository import AbstractRepository

def get_genres(repo: AbstractRepository):
    genres = repo.get_genres()
    genres.sort(key=lambda g: g.genre_name)
    return genres
