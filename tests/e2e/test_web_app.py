import pytest

from flask import session


def test_home(client):
    response = client.get('/')
    assert response.status_code == 200
    assert (b'<strong>Welcome </strong>to our ultimate gaming hub!') in response.data


def test_register(client):
    res_code = client.get('/authentication/register').status_code
    assert res_code == 200

    res = client.post(
        '/authentication/register',
        data={'username': 'xii', 'password': 'Xii123!'}
    )

    assert res.headers['Location'] == '/authentication/login'


@pytest.mark.parametrize(('username', 'password', 'message'), (
        ('', '', b'Your user name is required'),
        ('jp', '', b'Your user name is too short'),
        ('jason', '', b'Your password is required'),
        ('xii', 'test', b'Your password must be at least 6 characters long, and contain an uppercase letter, \
                       a lowercase letter, and a digit.'),
        ('jason', 'Jason123!', b'Your username is already taken - please pick another username.'),
))
def test_register_with_invalid_input(client, username, password, message):
    # Check that attempting to register with invalid combinations of username and password generate appropriate error
    # messages.
    response = client.post(
        '/authentication/register',
        data={'username': username, 'password': password}
    )
    assert message in response.data


def test_login(client, auth):
    # Check that we can retrieve the login page.
    status_code = client.get('/authentication/login').status_code
    assert status_code == 200

    # Check that a successful login generates a redirect to the homepage.
    response = auth.login()
    assert response.headers['Location'] == '/'

    # Check that a session has been created for the logged-in user.
    with client:
        client.get('/')
        assert session['username'] == 'jason'


@pytest.mark.parametrize(('username', 'password', 'message'), (
        ('unknownuser', 'thisuserHacking123', b'User name not recognised'),
        ('ray', 'Ray12344!', b'Password does not match supplied user name - please check and try again')))
def test_login_with_invalid_input(client, username, password, message):
    # Check that attempting to log in with invalid combinations of username and password generate appropriate error
    # messages.
    response = client.post(
        '/authentication/login',
        data={'username': username, 'password': password}
    )
    assert message in response.data


def test_logout(client, auth):
    # Login a user.
    auth.login()

    with client:
        # Check that logging out clears the user's session.
        auth.logout()
        assert 'user_id' not in session


def test_add_game_to_wishlist(client, auth):
    # Login a user.
    auth.login()

    # Check that we can retrieve the actions games page
    response = client.get('/browse_games?page=1&genre=Action')
    assert response.status_code == 200

    # Check that user can select a game to view its details
    response = client.get('/game-description/435790')
    assert response.status_code == 200

    # Check that the game description matches the one of game ID = 435790
    assert b'10 SECOND NINJA X' in response.data

    # Check that user clicks on add to favourites button Unsure about this one!!
    response = client.post('/toggle-favourite-game', data={'gameId': 435790})
    assert response.status_code == 302

    # Check that the game is in users wish list (which is in their profile)
    response = client.get('/my-profile')
    assert response.status_code == 200  # Assuming a success status code is returned.
    assert b'10 SECOND NINJA X' in response.data


def test_remove_game_from_wishlist(client, auth):
    # Login a user.
    auth.login()

    # Check that we can retrieve the actions games page
    response = client.get('/browse_games?page=1&genre=Action')
    assert response.status_code == 200

    # Check that user can select a game to view its details
    response = client.get('/game-description/435790')
    assert response.status_code == 200

    # Check that the game description matches the one of game ID = 435790
    assert b'10 SECOND NINJA X is a shockingly fast, overwhelmingly intense action/puzzle game.' in response.data

    # Check that user clicks on add to favourites button
    response = client.post('/toggle-favourite-game', data={'gameId': 435790})
    assert response.status_code == 302

    # Check that the game is in users wish list (which is in their profile)
    response = client.get('/my-profile')
    assert response.status_code == 200  # Assuming a success status code is returned.
    assert b'10 SECOND NINJA X' in response.data

    # Check that user clicks on same button again and it will remove the game from favourites. Unsure about this one!!
    response = client.post('/toggle-favourite-game', data={'gameId': 435790})
    assert response.status_code == 302

    # Check that the game is no longer in users wish list (which is in their profile)
    response = client.get('/my-profile')
    assert response.status_code == 200  # Assuming a success status code is returned.
    assert b'10 SECOND NINJA X' not in response.data


def test_add_favorite_game_not_logged_in(client):
    # User is not logged in.

    # Check that we can retrieve the actions games page
    response = client.get('/browse_games?page=1&genre=Action')
    assert response.status_code == 200

    # Check that user can select a game to view its details
    response = client.get('/game-description/435790')
    assert response.status_code == 200

    # Check that the game description matches the one of game ID = 435790
    assert b'10 SECOND NINJA X is a shockingly fast, overwhelmingly intense action/puzzle game.' in response.data

    # Check that user clicks on add to favorites button
    response = client.post('/toggle-favourite-game', data={'gameId': 435790})

    # Step 2: User is not logged in, so they should be redirected to the login page.
    assert response.status_code == 302
    assert response.headers['Location'] == '/authentication/login'


def test_can_browse_all_games_when_not_logged_in(client):
    response = client.get('/browse_games')
    assert response.status_code == 200

    # Step 2: User navigates to the last page using the Last button
    response = client.get('/browse_games?page=88')
    assert response.status_code == 200

    # Step 3: User clicks on a specific game
    response = client.get('/game-description/1304320')
    assert response.status_code == 200

    # Check that the game description matches the one of game ID = 1304320
    assert b'Metal Infinite' in response.data


def test_can_browse_all_games_when_logged_in(client, auth):
    # Step 1: User logs in.
    auth.login()

    response = client.get('/browse_games')
    assert response.status_code == 200

    # Step 2: User navigates to the last page using the Last button
    response = client.get('/browse_games?page=88')
    assert response.status_code == 200

    # Step 3: User clicks on a specific game
    response = client.get('/game-description/1304320')
    assert response.status_code == 200

    # Check that the game description matches the one of game ID = 1304320
    assert b'Metal Infinite' in response.data


def test_can_browse_games_filtered_by_genre(client):
    # Go to browse games by Action genre
    response = client.get('/browse_games?page=1&target_genre=Action')
    assert response.status_code == 200

    # Check that a game with Action genre is returned
    assert b'10 SECOND NINJA X' in response.data


def test_can_search_games_by_title(client):
    # Post a request to do a search
    response = client.post(
        '/search',
        data={'searchTerm': 'Ninja', 'searchCategory': 'title'}
    )
    assert response.status_code == 302

    # Follow the redirection to the games library screen
    redirection_location = response.headers['Location']
    redirected_response = client.get(redirection_location)

    # Check that the correct game is returned
    assert b'10 SECOND NINJA X' in redirected_response.data


def test_can_search_games_by_genre(client):
    # Post a request to do a search
    response = client.post(
        '/search',
        data={'searchTerm': 'Action', 'searchCategory': 'genre'}
    )
    assert response.status_code == 302

    # Follow the redirection to the games library screen
    redirection_location = response.headers['Location']
    redirected_response = client.get(redirection_location)

    # Check that the correct game is returned
    assert b'10 SECOND NINJA X' in redirected_response.data


def test_can_search_games_by_publisher(client):
    # Post a request to do a search
    response = client.post(
        '/search',
        data={'searchTerm': 'Curve Games', 'searchCategory': 'publisher'}
    )
    assert response.status_code == 302

    # Follow the redirection to the games library screen
    redirection_location = response.headers['Location']
    redirected_response = client.get(redirection_location)

    # Check that the correct game is returned
    assert b'10 SECOND NINJA X' in redirected_response.data


def test_search_games_none_returned(client):
    # Go to search games by publisher
    response = client.get('/browse_games?page=1&search_term=Apples&search_category=publisher')
    assert response.status_code == 200

    # Check that the correct game is returned
    assert b'No results' in response.data


def test_comment_can_be_added_when_logged_in(client, auth):
    # Login a user.
    auth.login()

    response = client.post(
        '/add_review',
        data={'gameId': 1304320, 'rating': 3, 'comment': 'Overall, this is a solid game with simple graphics and a '
                                                         'compelling story.'}
    )

    new_response = client.get('/my-profile')

    assert response.status_code == 302  # check that the user goes back to the same page after commenting

    # Check that the game is in users reviewed list (in their profile page)
    assert new_response.status_code == 200
    assert b'Metal Infinite' in new_response.data


def test_login_is_required_to_comment(client):
    response = client.post(
        '/add_review',
        data={'gameId': 435790, 'rating': 3, 'comment': 'Overall, this is a solid game with simple graphics and a '
                                                        'compelling story.'}
    )  # new review added without logging in
    assert response.headers['Location'] == '/authentication/login'
