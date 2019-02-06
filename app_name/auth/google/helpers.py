"""
Helper functions for Google Auth
"""
from pprint import pprint

import requests

from app_name import app

GOOGLE_TOKEN_INFO_ENDPOINT = 'https://www.googleapis.com/oauth2/v3/tokeninfo'
GOOGLE_OAUTH2_ENDPOINT = 'https://www.googleapis.com/oauth2/v4/token'


def get_google_access_token(auth_code, redirect_uri):
    """
    Gets Google access & refresh tokens using authorization code
    :param auth_code: str
    :param redirect_uri: str
    :return: google_access_token (str), google_refresh_token (str)
    """
    data = {
        'code': auth_code,
        'client_id': app.config.get('GOOGLE_CLIENT_ID'),
        'client_secret': app.config.get('GOOGLE_CLIENT_SECRET'),
        'redirect_uri': redirect_uri,
        'grant_type': 'authorization_code'
    }

    r = requests.post(GOOGLE_OAUTH2_ENDPOINT, data=data)

    token_data = r.json()

    pprint(token_data)

    token_info = get_google_token_info(token_data.get('access_token'), 'access_token')

    if r.ok and verify_google_access_token(token_data.get('access_token'), token_info):
        return token_data, token_info

    return None, None


def refresh_google_access_token(refresh_token):
    """
    Gets a new access token form Google
    :param refresh_token: str
    :return: google_access_token (str)
    """
    data = {
        'refresh_token': refresh_token,
        'client_id': app.config.get('GOOGLE_CLIENT_ID'),
        'client_secret': app.config.get('GOOGLE_CLIENT_SECRET'),
        'grant_type': 'refresh_token'
    }

    r = requests.post(GOOGLE_OAUTH2_ENDPOINT, data=data)

    token_data = r.json()
    token_info = get_google_token_info(token_data.get('access_token'), 'access_token')

    if r.ok and verify_google_access_token(token_data.get('access_token'), token_info):
        return token_data, token_info

    return None, None


def verify_google_access_token(google_access_token, token_info=None):
    """
    Verifies the Google access token and
    :param google_access_token:
    :param token_info:
    :return:
    """
    token_info = token_info or get_google_token_info(google_access_token, 'access_token')

    return token_info.get('aud') in app.config.get('GOOGLE_CLIENT_ID')


def get_google_token_info(google_token, token_type):
    """
    Gets user's info from Google
    :param google_token: str
    :param token_type: str
    :return:
    """
    params = {token_type: google_token}

    r = requests.get(GOOGLE_TOKEN_INFO_ENDPOINT, params=params)

    return r.json()
