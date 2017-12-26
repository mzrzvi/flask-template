"""
Helper functions for the Users module
"""
from app_name.users.models import (
    BaseUser,
    AdminUser,
    ExampleUser
)

_USER_ROLES = {
    'AdminUser': AdminUser,
    'ExampleUser': ExampleUser
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
    Will return None if the user type is not in the dict _USER_ROLES
    :rtype: object
    :param user_type: a str with the corresponding user type
    :return: the corresponding user db.Model object or None
    """
    return _USER_ROLES.get(user_type)


def get_all_user_types():
    """
    Returns all user type classes
    :return:
    """
    return [AdminUser, ExampleUser]


def get_user_by_email(email):
    """
    Finds user by email across all types
    Returns None if not found
    :param email:
    :return:
    """
    for UserType in get_all_user_types():
        user = UserType.query.filter_by(email=email).first()
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


def get_user_by_fb_id(fb_id):
    """
    Finds user by FB user id across all types
    Returns None if not found
    :param fb_id:
    :return:
    """
    for UserType in get_all_user_types():
        user = UserType.query.filter_by(facebook_user_id=fb_id).first()
        if user is not None:
            return user
