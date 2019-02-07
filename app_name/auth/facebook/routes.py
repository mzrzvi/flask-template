"""
Facebook auth routes
"""

# pylint: disable=no-member,invalid-name

from flask import request
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token
)

from . import helpers as fb

from app_name import app

from app_name.auth.email.helpers import confirm_email

from app_name.database import db

from app_name.users.models import User

from app_name.util import responses
from app_name.util.exceptions import protect_500


@app.route('/auth/signup/facebook', methods=['POST'])
@protect_500
def signup_facebook():
    """

    :return:
    """
    request_json = request.get_json()

    if not request_json:
        return responses.missing_params()

    user_token = request_json.get('user_token')
    user_type = request_json.get('user_type') or app.config.get('DEFAULT_USER_TYPE')

    if not all([user_token, user_type]):
        return responses.missing_params()

    # Get the access token again?
    access_token = fb.get_access_token(
        app_id=app.config.get('FACEBOOK_APP_ID'),
        app_secret=app.config.get('FACEBOOK_APP_SECRET')
    )

    token_info = fb.debug_user_token(user_token, access_token)

    if token_info.get('is_valid'):
        return responses.invalid_fb_token()

    fb_user_id = token_info.get('user_id')
    fb_user_info = fb.get_user_info(fb_user_id, user_token)

    # check that the user does not exist already in the database
    user_exists = db.session.query(
        db.exists().where(User.email == fb_user_info.get('email'))).scalar()

    if user_exists:
        return responses.user_already_exists()

    user = User(
        first_name=fb_user_info.get('first_name'),
        last_name=fb_user_info.get('last_name'),
        email=fb_user_info.get('email'),
        facebook_user_id=fb_user_id
    )

    db.session.add(user)
    db.session.commit()

    if not app.config.get('TESTING'):
        confirm_email(user)

    jwt_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)

    return responses.user_created(jwt_token, refresh_token)



@app.route('/auth/login/facebook', methods=['POST'])
@protect_500
def login_facebook():
    """
    Logs in user using Facebook OAuth
    Is user type agnostic
    :return:
    """
    request_json = request.get_json()

    if not request_json:
        return responses.missing_params()

    user_token = request_json.get('user_token')

    if not user_token:
        return responses.missing_params()

    # Get the access token again?
    access_token = fb.get_access_token(
        app_id=app.config.get('FACEBOOK_APP_ID'),
        app_secret=app.config.get('FACEBOOK_APP_SECRET')
    )

    token_info = fb.debug_user_token(user_token, access_token)

    if not token_info.get('is_valid'):
        return responses.invalid_fb_token()

    long_lived_token = fb.get_long_lived_token(
        app_id=app.config.get('FACEBOOK_APP_ID'),
        app_secret=app.config.get('FACEBOOK_APP_SECRET'),
        short_lived_token=user_token
    ).get('access_token')

    # get user id to look up in database?
    facebook_user_id = token_info.get('user_id')

    user = User.query.filter_by(facebook_user_id=facebook_user_id)

    if user is None:
        return responses.user_not_found()

    # check if current user token is the same if not change it
    if user.facebook_access_token != long_lived_token:
        user.facebook_access_token = long_lived_token

        db.session.commit()

    # Return app_name user access token for access to app_name api
    jwt_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)

    return responses.user_logged_in(jwt_token, refresh_token)

