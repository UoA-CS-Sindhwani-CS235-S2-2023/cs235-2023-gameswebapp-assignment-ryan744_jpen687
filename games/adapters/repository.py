import abc
from typing import List

from games.domainmodel.model import Publisher, Genre, Game

repo_instance = None


class RepositoryException(Exception):

    def __init__(self, message=None):
        pass


class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def add_publisher(self, publisher: Publisher):
        """" Adds a Publisher to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_publishers(self) -> List[Publisher]:
        """ Returns a list of Publishers from the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def add_genre(self, genre: Genre):
        """" Adds a Genre to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_genres(self) -> List[Genre]:
        """ Returns a list of Genres from the repository """
        raise NotImplementedError

    @abc.abstractmethod
    def add_game(self, game: Game):
        """" Adds a Game to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_game(self, id) -> Game:
        """ Returns the Game with the given id from the repository.

        If there is no Game with the given id, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_all_games(self):
        """Return a list of all the games in the repository."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_first_game(self):
        """Return the first Game Object"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_last_game(self):
        """Return thr last Game Object"""
        raise NotImplementedError
