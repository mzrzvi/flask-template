"""
All authentication endpoints used in the app
"""

# pylint: disable=no-member,invalid-name

from flask import request
from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity,
    jwt_refresh_token_required,
    create_refresh_token
)
from flask_security.utils import verify_password

from .helpers import confirm_email

from app_name import app
from app_name.database import db
from app_name.users.models import User

from app_name.util import responses
from app_name.util.exceptions import protect_500


@app.route('/auth/login/email', methods=['POST'])
@protect_500
def login():
    """
    Logs in user and returns access token
    :return:
    """
    request_json = request.get_json()

    email = request_json.get('email')
    password = request_json.get('password')

    if not all([email, password]):
        return responses.missing_params()

    user = User.query.filter_by(email=email).first()

    if user is None:
        return responses.user_not_found()

    if not verify_password(password, user.password):
        return responses.invalid_password()

    jwt_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)

    return responses.user_logged_in(jwt_token, refresh_token, user.id)


@app.route('/auth/signup/email', methods=['POST'])
@protect_500
def signup_email():
    """
    Signs up new user
    :return:
    """
    request_json = request.get_json()

    email = request_json.get('email')
    password = request_json.get('password')
    first_name = request_json.get('first_name')
    last_name = request_json.get('last_name')
    phone_number = request_json.get('phone_number')

    if not all([email, password, first_name, last_name]):
        return responses.missing_params()

    # check that the user does not exist already in the database
    user_exists = db.session.query(db.exists().where(User.email == email)).scalar()

    if user_exists:
        return responses.user_already_exists()

    user = User(
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=password,
        phone_number=phone_number
    )

    db.session.add(user)
    db.session.commit()

    if not app.config.get('TESTING'):
        confirm_email(user)

    # Return app_name user access token for access to app_name api
    # Identity can be any data that is json serializable
    jwt_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)

    return responses.user_created(jwt_token, refresh_token)


@app.route('/auth/refresh', methods=['POST'])
@protect_500
@jwt_refresh_token_required
def refresh():
    """
    Refreshes user token
    :return:
    """
    user_id = get_jwt_identity()
    new_token = create_access_token(identity=user_id)

    return responses.user_token_refreshed(new_token)
