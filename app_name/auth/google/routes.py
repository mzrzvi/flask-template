"""
Routes for Google Auth
"""

# pylint: disable=no-member,invalid-name

from flask import request

from app_name import app

from app_name.util import responses
from app_name.util.exceptions import protect_500


@app.route('/signup/google', methods=['POST'])
@protect_500
def signup_google():
    """

    :return:
    """
    request_json = request.get_json()

    if not request_json:
        return responses.missing_params()

    return None


@app.route('/login/google', methods=['POST'])
@protect_500
def login_facebook():
    """
    Logs in user using Google OAuth
    Is user type agnostic
    :return:
    """
    request_json = request.get_json()

    if not request_json:
        return responses.missing_params()

    return None
