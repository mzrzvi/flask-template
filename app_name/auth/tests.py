"""
Tests for User classes
"""

# pylint: disable=missing-docstring,invalid-name,no-member,attribute-defined-outside-init

import unittest
import json

from app_name.testing import AppTest


class RefreshTokenTests(AppTest):
    def test_refresh_token(self):
        signup_response = self.client.post('/signup/email', data=json.dumps({
            'email': 'me@johndoe.com',
            'password': 'pass12345',
            'first_name': 'John',
            'last_name': 'Doe'
        }), content_type='application/json', follow_redirects=True)

        refresh_response = self.client.post(
            '/auth/refresh',
            follow_redirects=True,
            headers={'Authorization': 'Bearer {}'.format(signup_response.json['app_refresh_token'])}
        )

        self.assertStatus(refresh_response, 201)


if __name__ == '__main__':
    unittest.main()
