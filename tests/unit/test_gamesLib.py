from games.gamesLib.services import get_batch_games, search_games_by_category, get_games_by_genre
from games.domainmodel.model import Publisher, Genre

def test_get_batch_games(in_memory_repo):
    assert len(get_batch_games(in_memory_repo)) == 7

def test_search_games_by_genre(in_memory_repo):
    assert len(search_games_by_category('Indie', 'genre', in_memory_repo)) == 2

def test_search_games_by_title(in_memory_repo):
    assert len(search_games_by_category('Ninja', 'title', in_memory_repo)) == 1

def test_search_games_by_publisher(in_memory_repo):
    assert len(search_games_by_category('Activision', 'publisher', in_memory_repo)) == 1

def test_get_games_by_genre(in_memory_repo):
    assert len(get_games_by_genre('Indie', in_memory_repo)) == 2

def test_multi_games_to_dict(in_memory_repo):
    ninja_game = search_games_by_category('Ninja', 'title', in_memory_repo)
    expected_output = [{
        'id': 435790,
        'date': 'Jul 19, 2016',
        'title': '10 Second Ninja X',
        'price': 0.99,
        'publisher': Publisher('Curve Games'),
        'summary': '10 SECOND NINJA X is a shockingly fast, overwhelmingly intense action/puzzle game. In this thumb blistering sequel, the nefarious Captain Greatbeard has kidnapped you and trapped your forest friends i...',
        'image_hyperlink': 'https://cdn.akamai.steamstatic.com/steam/apps/435790/header.jpg?t=1634742090',
        'genres': [ Genre('Action'), Genre('Indie') ]
    }]
    assert ninja_game == expected_output