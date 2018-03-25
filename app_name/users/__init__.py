"""
Initialize user module
"""

# pylint: disable=invalid-name

from flask_security import SQLAlchemyUserDatastore

from .models import BaseUser, Role

from app_name.database import db

datastore = SQLAlchemyUserDatastore(db, BaseUser, Role)
