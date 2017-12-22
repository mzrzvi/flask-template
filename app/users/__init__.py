"""
Initialize user module
"""

# pylint: disable=invalid-name

from flask_security import SQLAlchemyUserDatastore

from app.users.models import BaseUser, Role
from app.database import db

datastore = SQLAlchemyUserDatastore(db, BaseUser, Role)
