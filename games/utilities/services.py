from typing import Iterable
import random

from games.adapters.repository import AbstractRepository


def get_genres(repo: AbstractRepository):
    genres = repo.get_genres()
    if len(genres) > 0:
        genres.sort(key=lambda g: g.genre_name)
        return genres
