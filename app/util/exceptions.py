"""
Commonly used exceptions
"""
import traceback

from functools import wraps

from app.util import responses

class FBAuthException(Exception):
    """
    Exception to raise when Facebook auth fails
    """
    pass


def protect_500(func):
    """
    Wrapper around functions that prevents 500 response internal server errors
    :param func: function to be wrapped
    :return: wrapper
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(traceback.format_exc())
            return responses.server_error(e)

    return wrapper

