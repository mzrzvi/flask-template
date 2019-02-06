"""
Routes for Google Auth
"""

# pylint: disable=no-member,invalid-name

from flask import request, jsonify

from flask_jwt_extended import (
    create_access_token,
    create_refresh_token
)

from .helpers import get_google_access_token, get_google_token_info

from app_name import app

from app_name.database import db

from app_name.util import responses, status
from app_name.util.exceptions import protect_500

from app_name.users.models import User, OAuthConnection, OAuthConnectionType


@app.route('/auth/google/signup', methods=['POST'])
@protect_500
def signup_google():
    """
    Allows user to sign up via Google -- requires invite nonce
    :return: Response (object), status_code (int)
    """
    incoming = request.get_json() or {}

    required_attrs = ('code', 'invite_nonce')

    if not incoming or not all(attr in incoming for attr in required_attrs):
        return responses.missing_params()

    request_origin = request.environ.get('HTTP_ORIGIN')

    token_data, access_token_info = get_google_access_token(auth_code=incoming.get('code'),
                                                            redirect_uri=request_origin)

    if not token_data or not access_token_info:
        return jsonify({'error': 'Google Auth failed...'}), status.UNPROCESSABLE_ENTITY

    id_token_info = get_google_token_info(token_data.get('id_token'), 'id_token')
    oauth_email = id_token_info.get('email')

    user = User(
        email=oauth_email,
        image_url=id_token_info.get('picture')
    )

    oauth_connection = OAuthConnection(
        type=OAuthConnectionType.GOOGLE,
        email_address=oauth_email,
        ext_user_id=id_token_info.get('sub'),
        ext_access_token=token_data.get('access_token'),
        ext_refresh_token=token_data.get('refresh_token'),
    )

    user.oauth_connections.append(oauth_connection)
    db.session.add(oauth_connection)

    db.session.commit()

    jwt_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)

    user_info = dict(auth_type='google', **user.to_dict())

    return responses.user_logged_in(jwt_token, refresh_token, user.id, user_info=user_info)


@app.route('/auth/google/login', methods=['POST'])
@protect_500
def login_google():
    """
    Updates google_access_token for user
    :return: Response (object), status_code (int)
    """
    incoming = request.get_json() or {}

    required_attrs = ('code',)

    if not incoming or not all(attr in incoming for attr in required_attrs):
        return responses.missing_params()

    request_origin = request.environ.get('HTTP_ORIGIN')

    token_data, access_token_info = get_google_access_token(auth_code=incoming.get('code'),
                                                            redirect_uri=request_origin)

    if not token_data or not access_token_info:
        return jsonify({'error': 'Google Auth failed...'}), status.UNPROCESSABLE_ENTITY

    id_token_info = get_google_token_info(token_data.get('id_token'), 'id_token')
    oauth_email = id_token_info.get('email')

    user = User.query.filter_by(email=oauth_email).first()

    if not user:
        return responses.user_not_found()

    oauth_connection = OAuthConnection.query.filter_by(type=OAuthConnectionType.GOOGLE,
                                                       email_address=oauth_email).first()

    has_google_connection = oauth_connection is not None

    if not has_google_connection:
        oauth_connection = OAuthConnection()
        user.oauth_connections.append(oauth_connection)

        db.session.add(oauth_connection)

    oauth_connection.type = OAuthConnectionType.GOOGLE
    oauth_connection.email_address = oauth_email
    oauth_connection.ext_user_id = id_token_info.get('sub')
    oauth_connection.ext_access_token = token_data.get('access_token')
    oauth_connection.ext_refresh_token = token_data.get('refresh_token')

    db.session.commit()

    jwt_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)

    user_info = dict(auth_type='google', **user.to_dict())

    return responses.user_logged_in(jwt_token, refresh_token, user.id, user_info=user_info)
