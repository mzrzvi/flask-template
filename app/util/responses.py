"""
Commonly used responses
"""
from flask import jsonify

from app.util import status


def invalid_request_keys(invalid_keys):
    """
    Handles instance when the caller passes invalid keys in the
    request json
    :return:
    """
    return jsonify({
        'error': 'Invalid request keys: {}'.format(', '.join(invalid_keys))
    }), status.BAD_REQUEST


def missing_params():
    """
    Handles missing parameters in requests
    :return:
    """
    return jsonify({
        'error': 'Missing required params'
    }), status.BAD_REQUEST


def action_forbidden():
    """
    Handles cases where the action is forbidden
    :return:
    """
    return jsonify({
        'error': 'Action is forbidden'
    }), status.FORBIDDEN


def invalid_user_type(user_type):
    """
    Handles invalid user types
    :param user_type:
    :return:
    """
    return jsonify({
        'error': 'Invalid user type: {}'.format(user_type)
    }), status.BAD_REQUEST


def invalid_fb_token():
    """
    Handles case when user's FB token doesn't validate
    :return:
    """
    return jsonify({
        'error': 'Invalid facebook user token'
    }), status.BAD_REQUEST


def invalid_password():
    """
    Handles case when invalid password is used
    :return:
    """
    return jsonify({
        "error": "Invalid password"
    }), status.BAD_REQUEST


def user_created(jwt_token, refresh_token):
    """
    Handles case when user is created
    :return:
    """
    return jsonify({
        'app_access_token': jwt_token,
        'app_refresh_token': refresh_token,
        'message': 'User created successfully!'
    }), status.CREATED


def user_logged_in(jwt_token, refresh_token):
    """
    Handles case when user logs in
    :return:
    """
    return jsonify({
        'app_access_token': jwt_token,
        'app_refresh_token': refresh_token,
        'message': 'User logged in successfully!'
    }), status.OK


def user_already_exists():
    """
    Handles case when user who already exists tries to sign up
    :return:
    """
    return jsonify({
        'error': 'A user with that email already exists!'
    }), status.BAD_REQUEST


def user_not_found():
    """
    Handles case when user is not found
    :return:
    """
    return jsonify({
        "error": "User was not found"
    }), status.NOT_FOUND


def user_token_refreshed(jwt_token, refresh_token):
    """
    Handles case when user refreshes token
    :param jwt_token:
    :param refresh_token:
    :return:
    """
    return jsonify({
        'app_access_token': jwt_token,
        'app_refresh_token': refresh_token,
        'message': 'Token refreshed!'
    }), status.CREATED


def user_deleted():
    """
    Handles case when a user is deleted successfully
    :return: a json with one key value pair of message and success message string, and a
    OK (200) status
    """
    return jsonify({
        'message': 'User deleted successfully!'
    }), status.OK


def server_error(e):
    """
    Handles case when the server has an internal error
    :return: a json with one key value pair of message and error message string, and a
    Internal server error (500) status
    """
    return jsonify({
        'error': 'Internal server error: {}'.format(e)
    }), status.INTERNAL_SERVER_ERROR


def user_updated(password_changed=False):
    """
    Handles case when a user account is updated successfully
    :return: a json with one key value pair of message and success string message, and a
    created (201) status
    """
    return jsonify({
        'message': 'User updated successfully' +
                   (' and password changed' if password_changed else '')
    }), status.CREATED


def items_not_found():
    """
    Handles case when an endpoint is trying to find items based on some query and nothing
    was returned
    :return: (404) status and an error message
    """
    return jsonify({
        'message': 'No items were found!'
    }), status.NOT_FOUND
