from pathlib import Path

from bisect import insort_left

from games.adapters.repository import AbstractRepository
from games.adapters.datareader.csvdatareader import GameFileCSVReader
from games.domainmodel.model import User, Review


class MemoryRepository(AbstractRepository):
    # Games ordered by title.

    def __init__(self):
        self.__publishers = set()
        self.__genres = set()
        self.__games = []
        self.__games_index = dict()
        self.__users = list()
        self.__reviews = list()

    def add_user(self, user: User):
        self.__users.append(user)

    def get_user(self, username) -> User:
        return next((user for user in self.__users if user.username == username.lower()), None)

    def add_publisher(self, publisher):
        self.__publishers.add(publisher)

    def get_publishers(self):
        return list(self.__publishers)

    def add_genre(self, genre):
        self.__genres.add(genre)

    def get_genres(self):
        return list(self.__genres)

    def add_game(self, game):
        insort_left(self.__games, game, key=lambda x: x.title)
        self.__games_index[game.game_id] = game

    def get_game(self, id):
        for game in self.__games:
            if game.game_id == id:
                return game
        return None

    def get_first_game(self):
        game = None

        if len(self.__games) > 0:
            game = self.__games[0]
        return game

    def get_last_game(self):
        game = None

        if len(self.__games) > 0:
            game = self.__games[-1]
        return game

    def get_all_games(self):

        # Fetch the list of Games in Dictionary form.
        # all_games = [self.__games_index[id] for id in id_list]
        return list(self.__games)

    def add_review(self, new_review: Review):
        self.__reviews.append(new_review)

    def get_reviews(self):
        return self.__reviews
  
    def get_users_favourite_games(self, username):
        user = self.get_user(username)
        return user.favourite_games
  
    def add_users_favourite_game(self, username, game_id):
        user = self.get_user(username)
        game = self.get_game(game_id)
        user.add_favourite_game(game)

    def remove_users_favourite_game(self, username, game_id):
        user = self.get_user(username)
        game = self.get_game(game_id)
        user.remove_favourite_game(game)

def populate(data_path: Path, repo: MemoryRepository):
    reader = GameFileCSVReader(data_path)
    reader.read_csv_file()
    for game in reader.dataset_of_games:
        repo.add_game(game)
    for publisher in reader.dataset_of_publishers:
        repo.add_publisher(publisher)
    for genre in reader.dataset_of_genres:
        repo.add_genre(genre)
