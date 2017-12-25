"""
Routes for this resource group module
"""

from flask import request, jsonify

from flask_jwt_extended import jwt_required, get_jwt_identity

from app import app

from app.database import db

from app.util import status, responses
from app.util.exceptions import protect_500

from app.users.helpers import get_user_by_id

from app.resources.models import ResourceA


@app.route('/api/resource-a', methods=['POST'])
@protect_500
@jwt_required
def create_resource_a():
    """
    Returns current user's profile information
    :return:
    """
    user_id = get_jwt_identity()
    user = get_user_by_id(user_id)

    if user.type != 'example_user':
        return responses.action_forbidden()

    data = request.get_json()
    resource_a = ResourceA(**data)
    resource_a.owner_id = user_id

    user.resource_a_set.append(resource_a)

    db.session.add(resource_a)
    db.session.commit()

    return responses.resource_created('Resource A')


@app.route('/api/resource-a', methods=['GET'])
@protect_500
def get_all_resource_a():
    """
    Returns current user's profile information
    :return:
    """
    resource_a_set = ResourceA.query.all()

    return jsonify([resource_a.to_dict() for resource_a in resource_a_set]), status.OK


@app.route('/api/resource-a/<resource_a_id>', methods=['GET'])
@protect_500
def get_resource_a(resource_a_id):
    """
    Returns current user's profile information
    :return:
    """
    resource_a = ResourceA.query.get_or_404(resource_a_id)

    return jsonify(resource_a.to_dict()), status.OK


@app.route('/api/resource-a/<resource_a_id>', methods=['PUT'])
@protect_500
@jwt_required
def update_resource_a(resource_a_id):
    """
    Updates the user's profile based on attributes and values sent
    Can also change password
    :return:
    """
    resource_a = ResourceA.query.get_or_404(resource_a_id)

    user_id = get_jwt_identity()

    if user_id != resource_a.owner_id:
        return responses.unauthorized()

    valid_attrs = {'name'}

    update_attrs = request.get_json()

    if not update_attrs:
        return responses.missing_params()

    if not all(attr in valid_attrs for attr in update_attrs):
        return responses.invalid_request_keys(set(update_attrs) - valid_attrs)

    for attr, value in update_attrs.items():
        setattr(resource_a, attr, value)

    db.session.commit()

    return responses.resource_updated('Resource A')


@app.route('/api/resource-a/<resource_a_id>', methods=['DELETE'])
@protect_500
@jwt_required
def delete_resource_a(resource_a_id):
    """
    Deletes requester's account
    :return:
    """
    resource_a = ResourceA.query.get_or_404(resource_a_id)

    user_id = get_jwt_identity()

    if user_id != resource_a.owner_id:
        return responses.unauthorized()

    db.session.delete(resource_a)
    db.session.commit()

    return responses.resource_deleted('Resource A')