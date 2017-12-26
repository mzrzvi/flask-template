"""
Facebook helper functions
"""

# pylint: disable=no-member,invalid-name

import requests

from app_name.util import constants
from app_name.util.exceptions import FBAuthException

def get_access_token(app_id, app_secret):
    """
    Returns FB access_token
    :param app_id: str
    :param app_secret:  str
    :return: str
    """
    endpoint = '/oauth/access_token'

    params = {
        'client_id': app_id,
        'client_secret': app_secret,
        'grant_type': 'client_credentials'
    }

    url = constants.FB_GRAPH_API_URL + endpoint

    response = requests.get(url, params=params).json()

    if response.get('access_token'):
        return response.get('access_token')
    elif 'error' in response:
        raise FBAuthException(response.get('error').get('message'))


def debug_user_token(user_token, access_token):
    """
    Debugs FB user tokens
    :param user_token:
    :param access_token:
    :return:
    """
    endpoint = '/debug_token'

    params = {
        'input_token': user_token,
        'access_token': access_token
    }

    url = constants.FB_GRAPH_API_URL + endpoint
    response = requests.get(url, params=params).json()

    if 'data' in response:
        return response.get('data')
    elif 'error' in response:
        raise FBAuthException(response.get('error').get('message'))


def verify_user_token(*args, **kwargs):
    """
    Verifies FB user token
    :param args:
    :param kwargs:
    :return:
    """
    return debug_user_token(*args, **kwargs).get('is_valid')


def get_long_lived_token(app_id, app_secret, short_lived_token):
    """
    Gets and returns long lived token from Facebook
    :param app_id:
    :param app_secret:
    :param short_lived_token:
    :return: dict
    """

    endpoint = '/oauth/access_token'

    params = {
        'grant_type': 'fb_exchange_token',
        'client_id': app_id,
        'client_secret': app_secret,
        'fb_exchange_token': short_lived_token
    }

    url = constants.FB_GRAPH_API_URL + endpoint

    response = requests.get(url, params=params).json()

    return response


def get_user_info(user_id, access_token):
    """
    Facebook url reference: https://developers.facebook.com/docs/graph-api/reference/user/

    :param access_token:
    :param user_id: Facebook used id
    :return: dict
    """
    endpoint = '/v2.11/' + user_id

    params = {
        'fields': 'first_name,last_name,email'
    }

    headers = {
        'Authorization': 'Bearer ' + access_token
    }

    url = constants.FB_GRAPH_API_URL + endpoint
    response = requests.get(url, params=params, headers=headers).json()

    return response
