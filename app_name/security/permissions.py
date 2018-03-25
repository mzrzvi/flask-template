"""
Resources permissions per user type
"""
from app_name.resources.models import ResourceA

from app_name.security.constants import CREATE, VIEW, VIEW_ALL

PERMISSIONS = {
    ResourceA.__name__: {
        CREATE: {'admin'},
        VIEW: {'admin', 'example_user'},
        VIEW_ALL: {'admin'},
    }
}


def check_permission(user_type, permission, resource_name):
    """
    Utility function to determine if the user can access a resource in a certain way
    :param user_type:
    :param permission:
    :param resource_name:
    :return:
    """
    return user_type in PERMISSIONS[resource_name][permission]
