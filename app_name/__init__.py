"""
Configuration for Flask App
"""

# pylint: disable=invalid-name,no-member,wrong-import-position

from flask import Flask
from flask_mail import Mail

from app_name import config

app = Flask(__name__)
app.config.from_object(config.get_config())

mail = Mail(app)

# Import routes
from app_name.admin import routes as admin_routes
from app_name.auth.email import routes as auth_routes
from app_name.auth.facebook import routes as fb_routes
from app_name.users import routes as user_routes
from app_name.resources import routes as resource_routes
from app_name.security import security as app_security


def get_app():
    """
    Returns the instance of the Flask app_name
    :return: Flask app_name
    """
    return app
