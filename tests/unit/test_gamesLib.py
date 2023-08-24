from games.gamesLib.services import filter_games
from games.domainmodel.model import Publisher, Genre, Game, Review, User, Wishlist

def test_filter_games_search_term_none():
    batch_of_games = [{'title': 'Game 1', 'genres': [Genre('Action')]},
                      {'title': 'Game 2', 'genres': [Genre('Adventure')]}]
    search_term = None
    search_category = 'genre'
    
    result = filter_games(batch_of_games, search_term, search_category)
    
    assert result == batch_of_games

def test_filter_games_by_genre():
    batch_of_games = [{'title': 'Game 1', 'genres': [Genre('Action')]},
                      {'title': 'Game 2', 'genres': [Genre('Adventure')]}]
    search_term = 'Action'
    search_category = 'genre'
    
    result = filter_games(batch_of_games, search_term, search_category)
    
    assert result == [{'title': 'Game 1', 'genres': [Genre('Action')]}]

def test_filter_games_by_genre_search_term_lower():
    batch_of_games = [{'title': 'Game 1', 'genres': [Genre('Action')]},
                      {'title': 'Game 2', 'genres': [Genre('Adventure')]}]
    search_term = 'action'
    search_category = 'genre'
    
    result = filter_games(batch_of_games, search_term, search_category)
    
    assert result == [{'title': 'Game 1', 'genres': [Genre('Action')]}]

def test_filter_games_by_title():
    batch_of_games = [{'title': 'Game 1', 'genres': [Genre('Action')]},
                      {'title': 'Game 2', 'genres': [Genre('Adventure')]}]
    search_term = 'Game 2'
    search_category = 'title'
    
    result = filter_games(batch_of_games, search_term, search_category)
    
    assert result == [{'title': 'Game 2', 'genres': [Genre('Adventure')]}]

def test_filter_games_by_title_search_term_lower():
    batch_of_games = [{'title': 'Game 1', 'genres': [Genre('Action')]},
                      {'title': 'Game 2', 'genres': [Genre('Adventure')]}]
    search_term = 'game 2'
    search_category = 'title'
    
    result = filter_games(batch_of_games, search_term, search_category)
    
    assert result == [{'title': 'Game 2', 'genres': [Genre('Adventure')]}]

def test_filter_games_by_publisher():
    batch_of_games = [{'title': 'Game 1', 'publisher': Publisher('Publisher A')},
                      {'title': 'Game 2', 'publisher': Publisher('Publisher B')}]
    search_term = 'Publisher A'
    search_category = 'publisher'
    
    result = filter_games(batch_of_games, search_term, search_category)
    
    assert result == [{'title': 'Game 1', 'publisher': Publisher('Publisher A')}]

def test_filter_games_by_publisher_search_term_lower():
    batch_of_games = [{'title': 'Game 1', 'publisher': Publisher('Publisher A')},
                      {'title': 'Game 2', 'publisher': Publisher('Publisher B')}]
    search_term = 'publisher a'
    search_category = 'publisher'
    
    result = filter_games(batch_of_games, search_term, search_category)
    
    assert result == [{'title': 'Game 1', 'publisher': Publisher('Publisher A')}]

def test_filter_games_no_match():
    batch_of_games = [{'title': 'Game 1', 'genres': [Genre('Action')]},
                      {'title': 'Game 2', 'genres': [Genre('Adventure')]}]
    search_term = 'Strategy'
    search_category = 'genre'
    
    result = filter_games(batch_of_games, search_term, search_category)
    
    assert result == []