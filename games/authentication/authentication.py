from flask import Blueprint, render_template, redirect, url_for, session

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError

from password_validator import PasswordValidator

from functools import wraps

import games.utilities.utilities as utilities
import games.authentication.services as services
import games.adapters.repository as repo

# Configure Blueprint.
authentication_blueprint = Blueprint(
    'authentication_bp', __name__, url_prefix='/authentication')


@authentication_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = CustomRegistrationForm()
    non_unique_username = None
    if form.validate_on_submit():
        # Successful POST, i.e. the username and password have passed validation checking.
        # Use the service layer to attempt to add the new user.
        try:
            services.add_user(form.username.data, form.password.data, repo.repo_instance)

            # Initialise session and redirect the user to the home page.
            session.clear()
            session['username'] = form.username.data;
            return redirect(url_for('home_bp.home'))
        except services.NameNotUniqueException:
            non_unique_username = 'Your username is already taken - please pick another username.'

    # For a GET or a failed POST request, return the Registration Web page.
    return render_template(
        'authentication/credentials.html',
        title='Register form',
        form=form,
        user_name_error_message=non_unique_username,
        handler_url=url_for('authentication_bp.register'),
        genres=utilities.get_genres(),
        logged_in_username=logged_in_username(),
    )


@authentication_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = CustomLoginForm()
    unrecognised_user = None
    unmatched_pass_and_user = None

    if form.validate_on_submit():
        # Successful POST, i.e. the username and password have passed validation checking.
        # Use the service layer to look up the user.
        try:
            user = services.get_user(form.username.data, repo.repo_instance)

            # Authenticate user.
            services.authenticate_user(user['username'], form.password.data, repo.repo_instance)

            # Initialise session and redirect the user to the home page.
            session.clear()
            session['username'] = user['username']
            return redirect(url_for('home_bp.home'))

        except services.UnknownUserException:
            # Username not known to the system, set a suitable error message.
            unrecognised_user = 'User name not recognised'

        except services.AuthenticationException:
            # Authentication failed, set a suitable error message.
            unmatched_pass_and_user = 'Password does not match supplied user name - please check and try again'

    # For a GET or a failed POST, return the Login Web page.
    return render_template(
        'authentication/credentials.html',
        title='Login',
        user_name_error_message=unrecognised_user,
        password_error_message=unmatched_pass_and_user,
        form=form,
        genres=utilities.get_genres(),
        logged_in_username=logged_in_username(),
    )


@authentication_blueprint.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home_bp.home'))


def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if 'username' not in session:
            return redirect(url_for('authentication_bp.login'))
        try:
          services.get_user(session['username'], repo.repo_instance)
        except services.UnknownUserException: 
            return redirect(url_for('authentication_bp.login'))
        return view(**kwargs)

    return wrapped_view

def logged_in_username():
    if 'username' not in session:
        return None;
    try:
      user = services.get_user(session['username'], repo.repo_instance)
      return user['username'];
    except services.UnknownUserException: 
        return None;

class CustomPasswordValidator:
    def __init__(self, message=None):
        if not message:
            message = u'Your password must be at least 6 characters long, and contain an uppercase letter, \
                       a lowercase letter, and a digit.'
        self.message = message

    def __call__(self, form, field):
        schema = PasswordValidator()
        schema \
            .min(6) \
            .has().uppercase() \
            .has().lowercase() \
            .has().digits()
        if not schema.validate(field.data):
            raise ValidationError(self.message)


class CustomRegistrationForm(FlaskForm):
    username = StringField('New Username', [
        DataRequired(message='Your user name is required'),
        Length(min=3, message='Your user name is too short')])
    password = PasswordField('New Password', [
        DataRequired(message='Your password is required'),
        CustomPasswordValidator()])
    submit = SubmitField('Register')


class CustomLoginForm(FlaskForm):
    username = StringField('Enter your Username', [
        DataRequired()])
    password = PasswordField('Enter your Password', [
        DataRequired()])
    submit = SubmitField('Login')
