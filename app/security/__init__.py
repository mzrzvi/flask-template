"""
Flask security variables and functions
"""

# pylint: disable=invalid-name,wrong-import-position

from flask import url_for
from flask_admin import helpers as admin_helpers
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_security import Security

from app import app
from app.admin import admin
from app.users import datastore

security = Security(app, datastore)

bcrypt = Bcrypt(app)

jwt = JWTManager(app)

cors = CORS(app, resources={r'*': {'origins': '*'}})


@security.context_processor
def security_context_processor():
    """
    Processes context of admin panel access
    :return:
    """
    return dict(
        admin_base_template=admin.base_template,
        admin_view=admin.index_view,
        h=admin_helpers,
        get_url=url_for
    )
