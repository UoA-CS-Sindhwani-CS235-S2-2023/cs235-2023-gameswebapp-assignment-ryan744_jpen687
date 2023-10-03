from abc import ABC
from typing import List

from sqlalchemy.orm import scoped_session
from sqlalchemy.orm.exc import NoResultFound

from games.adapters.repository import AbstractRepository
from games.domainmodel.model import Game, Publisher, Genre, User, Review


class SessionContextManager:
    def __init__(self, session_factory):
        self.__session_factory = session_factory
        self.__session = scoped_session(self.__session_factory)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @property
    def session(self):
        return self.__session

    def commit(self):
        self.__session.commit()

    def rollback(self):
        self.__session.rollback()

    def reset_session(self):
        # this method can be used e.g. to allow Flask to start a new session for each http request,
        # via the 'before_request' callback
        self.close_current_session()
        self.__session = scoped_session(self.__session_factory)

    def close_current_session(self):
        if not self.__session is None:
            self.__session.close()


class SqlAlchemyRepository(AbstractRepository, ABC):

    def __init__(self, session_factory):
        self._session_cm = SessionContextManager(session_factory)

    def close_session(self):
        self._session_cm.close_current_session()

    def reset_session(self):
        self._session_cm.reset_session()

    def get_games(self) -> List[Game]:
        games = self._session_cm.session.query(Game).order_by(Game._Game__game_id).all()
        return games

    def get_game(self, game_id: int) -> Game:
        game = None
        try:
            game = self._session_cm.session.query(
                Game).filter(Game._Game__game_id == game_id).one()
        except NoResultFound:
            print(f'Game {game_id} was not found')

        return game

    def add_game(self, game: Game):
        with self._session_cm as scm:
            scm.session.merge(game)
            scm.commit()

    def add_multiple_games(self, games: List[Game]):
        with self._session_cm as scm:
            for game in games:
                scm.session.merge(game)
            scm.commit()

    def get_number_of_games(self):
        total_games = self._session_cm.session.query(Game).count()
        return total_games

    def get_publishers(self) -> List[Publisher]:
        pass

    def add_publisher(self, publisher: Publisher):
        with self._session_cm as scm:
            scm.session.merge(publisher)
            scm.commit()

    def add_multiple_publishers(self, publishers: List[Publisher]):
        with self._session_cm as scm:
            for publisher in publishers:
                scm.session.merge(publisher)
            scm.commit()

    def get_number_of_publishers(self) -> int:
        pass


    def get_genres(self) -> List[Genre]:
        genres = self._session_cm.session.query(Genre).order_by(Genre._Genre__genre_name).all()
        return genres

    def add_genre(self, genre: Genre):
        with self._session_cm as scm:
            scm.session.merge(genre)
            scm.commit()

    def add_multiple_genres(self, genres: List[Genre]):
        with self._session_cm as scm:
            for genre in genres:
                scm.session.merge(genre)
            scm.commit()


    def search_games_by_title(self, title_string: str) -> List[Game]:
        pass

    def add_review(self, new_review: Review):
        pass

    def add_user(self, user: User):
        with self._session_cm as scm:
            scm.session.merge(user)
            scm.commit()

    def get_all_games(self):
        pass

    def get_first_game(self):
        pass

    def get_last_game(self):
        pass

    def get_reviews(self):
        pass

    def add_users_favourite_game(self, username, game_id):
        user = self.get_user(username)
        game = self.get_game(game_id)
        user.add_favourite_game(game)
        with self._session_cm as scm:
            scm.session.merge(user)
            scm.commit()

    def get_user(self, username) -> User:
        user = None
        try:
            user = self._session_cm.session.query(
                User).filter(User._User__username == username).one()
        except NoResultFound:
            print(f'User {username} was not found')

        return user

    def get_users_favourite_game_ids(self, username):
        rows = self._session_cm.session.execute('SELECT game_id FROM favourites WHERE username = :username', {'username': username}).all()
        game_ids = [game_id[0] for game_id in rows]
        return game_ids

    def remove_users_favourite_game(self, username, game_id):
        user = self.get_user(username)
        game = self.get_game(game_id)
        user.remove_favourite_game(game)
        with self._session_cm as scm:
            scm.session.merge(user)
            scm.commit()

    def search_games_by_genre(self, search_term):
        pass

    def search_games_by_publisher(self, search_term):
        pass