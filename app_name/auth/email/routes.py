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
from app_name.users.helpers import (
    get_user_type,
    get_admin_user_type
)
from app_name.users.models import BaseUser

from app_name.util import responses
from app_name.util.exceptions import protect_500


@app.route('/login/email', methods=['POST'])
@protect_500
def login():
    """
    Provide a method to create access tokens. The create_access_token()
    function is used to actually generate the token, and you can return
    it to the caller however you choose.
    :return:
    """
    request_json = request.get_json()

    email = request_json.get('email')
    password = request_json.get('password')

    if not all([email, password]):
        return responses.missing_params()

    user = BaseUser.get_user_by_attrs(email=email)

    if user is None:
        return responses.user_not_found()

    if not verify_password(password, user.password):
        return responses.invalid_password()

    jwt_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)

    return responses.user_logged_in(jwt_token, refresh_token)


@app.route('/signup/email', methods=['POST'])
@protect_500
def signup_email():
    """

    :return:
    """

    request_json = request.get_json()

    email = request_json.get('email')
    password = request_json.get('password')
    first_name = request_json.get('first_name')
    last_name = request_json.get('last_name')
    phone_number = request_json.get('phone_number')
    user_type = request_json.get('user_type') or app.config.get('DEFAULT_USER_TYPE')

    if not all([email, password, first_name, last_name]):
        return responses.missing_params()

    UserType = get_user_type(user_type)

    if UserType is None:
        return responses.invalid_user_type(user_type)

    # Only allow admin creation in admin panel
    if UserType is get_admin_user_type():
        return responses.action_forbidden()

    # check that the user does not exist already in the database
    user_exists = db.session.query(db.exists().where(UserType.email == email)).scalar()

    if user_exists:
        return responses.user_already_exists()

    user = UserType(first_name=first_name,
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


@app.route('/refresh', methods=['POST'])
@protect_500
@jwt_refresh_token_required
def refresh():
    """
    Refreshes user token
    :return:
    """
    user_id = get_jwt_identity()
    jwt_token = create_access_token(identity=user_id)
    refresh_token = create_refresh_token(identity=user_id)

    return responses.user_token_refreshed(jwt_token, refresh_token)
