from flask_testing import TestCase

from app import app
from app.database import db


class AppTest(TestCase):
    def create_app(self):
        self.app = app
        self.app.config.from_object('app.config.TestingConfig')
        self.app.testing = True
        self.client = app.test_client()

        return self.app

    def setUp(self):
        self.db = db
        self.db.create_all()

    def tearDown(self):
        self.db.session.remove()
        self.db.drop_all()