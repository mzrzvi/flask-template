"""
Helper functions for the Users module
"""
from sqlalchemy.sql.expression import and_

from .models import (
    BaseUser,
    AdminUser,
    ExampleUser
)

from .constants import ADMIN, EXAMPLE_USER

USER_TYPES = {
    ADMIN: AdminUser,
    EXAMPLE_USER: ExampleUser
}


def get_admin_user_type():
    """
    Returns Admin User type
    :return:
    """
    return AdminUser


def get_user_type(user_type: str) -> type(BaseUser):
    # type: (str) -> type(BaseUser)
    """
    Helper function for getting the correct User object in routes
    Will return None if the user type is not in the dict USER_TYPES
    :rtype: object
    :param user_type: a str with the corresponding user type
    :return: the corresponding user db.Model object or None
    """
    return USER_TYPES.get(user_type)


def get_all_user_types():
    """
    Returns all user type classes
    :return:
    """
    return USER_TYPES.values()


def get_user_by_attrs(get_all=False, **attrs):
    """
    Filters users by provided attributes
    Provided attributes must be in BaseUser class
    :param kwargs: dict()
    :return: user
    """
    for UserType in get_all_user_types():
        user = UserType.get_user_by_attrs(get_all, **attrs)
        if user is not None:
            return user


def get_user_by_id(user_id):
    """
    Finds user by user id across all types
    Returns None if not found
    :param user_id:
    :return:
    """
    for UserType in get_all_user_types():
        user = UserType.query.get(user_id)
        if user is not None:
            return user
