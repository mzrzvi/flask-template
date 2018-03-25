"""
Superclass for tests
"""

from flask_testing import TestCase

from app_name import app
from app_name.database import db


class AppTest(TestCase):
    def create_app(self):
        self.app = app
        self.app.config.from_object('app_name.config.TestingConfig')
        self.app.testing = True
        self.client = app.test_client()

        return self.app

    def setUp(self):
        self.db = db
        self.db.create_all()

    def tearDown(self):
        self.db.session.remove()
        self.db.drop_all()