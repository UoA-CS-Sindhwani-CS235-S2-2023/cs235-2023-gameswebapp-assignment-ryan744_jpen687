import abc
from typing import List

from games.domainmodel.model import Publisher, Genre, Game, User, Review

repo_instance = None


class RepositoryException(Exception):

    def __init__(self, message=None):
        pass


class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def add_user(self, user: User):
        """" Adds a User to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_user(self, username) -> User:
        """ Returns the User named username from the repository.

        If there is no User with the given username, this method returns None.
        """
        raise NotImplementedError

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

    @abc.abstractmethod
    def add_review(self, new_review: Review):
        """ Adds a review (comment + rating) to the repository.

        If the Review doesn't have links with a User, this method raises a
        RepositoryException and doesn't update the repository.
        """
        if new_review.user is None or new_review not in new_review.user.reviews:
            raise RepositoryException('Review not correctly attached to a User')

    @abc.abstractmethod
    def get_reviews(self):
        """ Returns the Reviews stored in the repository. """
        raise NotImplementedError
    
    @abc.abstractmethod
    def get_users_favourite_games(self, username):
        """ Returns the favourite games for a user stored in the repository. """
        raise NotImplementedError
  
    @abc.abstractmethod
    def add_users_favourite_game(self, username, game_id):
        """ Adds the game with the specified game_id into the favourite games list for the user """
        raise NotImplementedError
  
    @abc.abstractmethod
    def remove_users_favourite_game(self, username, game_id):
        """ Remove the game with the specified game_id from the favourite games list for the user """
        raise NotImplementedError
    
    @abc.abstractmethod
    def search_games_by_genre(self, search_term):
        """ Find games with a genre that matches the search term """
        raise NotImplementedError
    
    @abc.abstractmethod
    def search_games_by_title(self, search_term):
        """ Find games with a title that matches the search term """
        raise NotImplementedError
    
    @abc.abstractmethod
    def search_games_by_publisher(self, search_term):
        """ Find games with a publisher that matches the search term """
        raise NotImplementedError