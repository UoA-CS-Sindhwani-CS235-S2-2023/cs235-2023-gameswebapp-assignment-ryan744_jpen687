from pathlib import Path

from bisect import insort_left

from games.adapters.repository import AbstractRepository
from games.adapters.datareader.csvdatareader import GameFileCSVReader


class MemoryRepository(AbstractRepository):
    # Games ordered by title.

    def __init__(self):
        self.__publishers = set()
        self.__genres = set()
        self.__games = []
        self.__games_index = dict()

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


def populate(data_path: Path, repo: MemoryRepository):
    reader = GameFileCSVReader(data_path)
    reader.read_csv_file()
    for game in reader.dataset_of_games:
        repo.add_game(game)
    for publisher in reader.dataset_of_publishers:
        repo.add_publisher(publisher)
    for genre in reader.dataset_of_genres:
        repo.add_genre(genre)