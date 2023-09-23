from games.authentication.services import add_user, get_user, authenticate_user, NameNotUniqueException, AuthenticationException, UnknownUserException

import pytest

def test_can_add_user(in_memory_repo):
    new_username = 'jz'
    new_password = 'abcd1A23'

    add_user(new_username, new_password, in_memory_repo)

    user_as_dict = get_user(new_username, in_memory_repo)
    assert user_as_dict['username'] == new_username

    # Check that password has been encrypted.
    assert user_as_dict['password'].startswith('pbkdf2:sha256:')


def test_cannot_add_user_with_existing_name(in_memory_repo):
    username = 'jason'
    password = 'Jason123!'

    with pytest.raises(NameNotUniqueException):
        add_user(username, password, in_memory_repo)

def test_cannot_get_user_that_does_not_exist(in_memory_repo):
    with pytest.raises(UnknownUserException):
        get_user('xi', in_memory_repo)

def test_authentication_with_valid_credentials(in_memory_repo):
    new_username = 'xi'
    new_password = 'xi1234!'

    add_user(new_username, new_password, in_memory_repo)

    try:
        authenticate_user(new_username, new_password, in_memory_repo)
    except AuthenticationException:
        assert False


def test_authentication_with_invalid_credentials(in_memory_repo):
    new_username = 'xi'
    new_password = 'abcd1A23'

    add_user(new_username, new_password, in_memory_repo)

    with pytest.raises(AuthenticationException):
        authenticate_user(new_username, '0987654321', in_memory_repo)