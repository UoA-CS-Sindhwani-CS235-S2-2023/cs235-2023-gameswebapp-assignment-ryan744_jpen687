from games.gamesLib.services import multi_games_to_dict

def get_favourite_games(username, repo):
  user = repo.get_user(username);
  return multi_games_to_dict(user.favourite_games)