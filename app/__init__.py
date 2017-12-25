"""
Configuration for Flask App
"""

# pylint: disable=invalid-name,no-member,wrong-import-position

from flask import Flask
from flask_mail import Mail

from app import config

app = Flask(__name__)
app.config.from_object(config.get_config())

mail = Mail(app)

# Import routes
from app.admin import routes as admin_routes
from app.auth.email import routes as auth_routes
from app.auth.facebook import routes as fb_routes
from app.users import routes as user_routes
from app.resources import routes as resource_routes
from app.security import security as app_security


def get_app():
    """
    Returns the instance of the Flask app
    :return: Flask app
    """
    return app
