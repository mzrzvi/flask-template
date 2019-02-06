"""
Endpoints for user CRUD excluding signup
"""
from flask import request, jsonify

from flask_jwt_extended import jwt_required, get_jwt_identity

from .models import User

from app_name import app

from app_name.database import db

from app_name.util import status, responses
from app_name.util.exceptions import protect_500


@app.route('/users/<user_id>', methods=['GET'])
@protect_500
def get_public_profile(user_id):
    """
    Returns user's profile information based on user_id provided
    :return:
    """
    user = User.query.get(user_id)

    if not user:
        return responses.user_not_found()

    return jsonify(user.public_dict()), status.OK


@app.route('/users/me', methods=['GET'])
@protect_500
@jwt_required
def get_my_profile():
    """
    Returns current user's profile information
    :return:
    """
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return responses.user_not_found()

    return jsonify(user.to_dict()), status.OK


@app.route('/users/me', methods=['PUT'])
@protect_500
@jwt_required
def update_profile():
    """
    Updates the user's profile based on attributes and values sent
    Can also change password
    :return:
    """
    valid_attrs = {'first_name', 'last_name', 'email', 'phone_number', 'new_password',
                   'old_password'}

    update_attrs = request.get_json()

    if not update_attrs:
        return responses.missing_params()

    if not all(attr in valid_attrs for attr in update_attrs):
        return responses.invalid_request_keys(set(update_attrs) - valid_attrs)

    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return responses.user_not_found()

    changed = False
    if 'new_password' in update_attrs and 'old_password' in update_attrs:
        old_password = update_attrs.pop('old_password')
        new_password = update_attrs.pop('new_password')

        changed = user.change_password(old_password, new_password)

        if not changed:
            return responses.invalid_password()

    for attr, value in update_attrs.items():
        setattr(user, attr, value)

    db.session.commit()

    return responses.user_updated(password_changed=changed)


@app.route('/users/me', methods=['DELETE'])
@protect_500
@jwt_required
def delete_profile():
    """
    Deletes requester's account
    :return:
    """
    user_id = get_jwt_identity()

    user = User.query.get(user_id)

    if not user:
        return responses.user_not_found()

    db.session.delete(user)
    db.session.commit()

    return responses.resource_deleted(User.__name__)
