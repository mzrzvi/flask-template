"""
Tests for User classes
"""

# pylint: disable=missing-docstring,invalid-name,no-member,attribute-defined-outside-init

import unittest
import json

from flask_testing import TestCase

from app.database import db

from app import app


class RefreshTokenTests(TestCase):
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

    def test_refresh_token(self):
        signup_response = self.client.post('/signup/email', data=json.dumps({
            'email': 'me@johndoe.com',
            'password': 'pass12345',
            'first_name': 'John',
            'last_name': 'Doe'
        }), content_type='application/json', follow_redirects=True)

        refresh_response = self.client.post('/refresh',
                                            follow_redirects=True,
                                            headers={'authorization': 'Bearer {}'.format(
                                                signup_response.json['app_refresh_token'])}
                                            )

        self.assertStatus(refresh_response, 201)


if __name__ == '__main__':
    unittest.main()
