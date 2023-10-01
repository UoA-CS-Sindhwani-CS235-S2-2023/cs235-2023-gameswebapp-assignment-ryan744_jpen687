import csv
from pathlib import Path

from bisect import insort_left

from games.adapters.repository import AbstractRepository
from games.adapters.datareader.csvdatareader import GameFileCSVReader
from games.domainmodel.model import User, Review

from werkzeug.security import generate_password_hash


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
        if user is None:
            return []
        return user.favourite_games

    def add_users_favourite_game(self, username, game_id):
        user = self.get_user(username)
        game = self.get_game(game_id)
        user.add_favourite_game(game)

    def remove_users_favourite_game(self, username, game_id):
        user = self.get_user(username)
        game = self.get_game(game_id)
        user.remove_favourite_game(game)

    def search_games_by_genre(self, search_term):
        def filter_fn(game):
            genre_names = map(lambda x: x.genre_name.lower(), game.genres)
            if search_term.lower() in genre_names:
                return True

        return list(filter(filter_fn, self.__games))

    def search_games_by_title(self, search_term):
        def filter_fn(game):
            if search_term.lower() in game.title.lower():
                return True

        return list(filter(filter_fn, self.__games))

    def search_games_by_publisher(self, search_term):
        def filter_fn(game):
            if search_term.lower() in game.publisher.publisher_name.lower():
                return True

        return list(filter(filter_fn, self.__games))


def read_csv_file(filename: str):
    with open(filename, encoding='utf-8-sig') as infile:
        reader = csv.reader(infile)

        # Read first line of the CSV file.
        headers = next(reader)

        # Read remaining rows from the CSV file.
        for row in reader:
            # Strip any leading/trailing white space from data read.
            row = [item.strip() for item in row]
            yield row


def load_users(data_path: Path, repo: AbstractRepository):
    users = dict()

    users_filename = str(Path(data_path) / "users.csv")
    for data_row in read_csv_file(users_filename):
        user = User(
            username=data_row[1],
            password=generate_password_hash(data_row[2])
        )
        repo.add_user(user)
        users[data_row[0]] = user
    return users


def load_games(data_path: Path, repo: AbstractRepository):
    reader = GameFileCSVReader(Path(data_path) / 'games.csv')
    reader.read_csv_file()
    for game in reader.dataset_of_games:
        repo.add_game(game)
    for publisher in reader.dataset_of_publishers:
        repo.add_publisher(publisher)
    for genre in reader.dataset_of_genres:
        repo.add_genre(genre)


def populate(data_path: Path, repo: AbstractRepository):
    load_games(data_path, repo)

    load_users(data_path, repo)
