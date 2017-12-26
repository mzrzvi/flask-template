"""
Tests for User classes
"""

# pylint: disable=missing-docstring,invalid-name,no-member,attribute-defined-outside-init

import json
import unittest

from app_name.testing import AppTest
from app_name.users.models import AdminUser


class AdminUserTest(AppTest):
    def test_admin_user1(self):
        user = AdminUser(
            first_name='John',
            last_name='Smith',
            email='john.smith@example.com',
            password='password',
            is_active=True
        )

        self.db.session.add(user)

        q_user = AdminUser.query.filter_by(first_name='John').first()

        self.assertEqual(user, q_user)

    def test_email_signup(self):
        response = self.client.post('/signup/email', data=json.dumps({
            'email': 'me@johndoe.com',
            'password': 'pass12345',
            'first_name': 'John',
            'last_name': 'Doe',
            'user_type': 'AdminUser'
        }), content_type='application/json', follow_redirects=True)

        self.assert_status(response, 403)


class ExampleUserTest(AppTest):
    def test_signup(self):
        response = self.client.post('/signup/email', data=json.dumps({
            'email': 'me@johndoe.com',
            'password': 'pass12345',
            'first_name': 'John',
            'last_name': 'Doe'
        }), content_type='application/json', follow_redirects=True)

        self.assert_status(response, 201)

    def test_delete(self):
        signup_response = self.client.post('/signup/email', data=json.dumps({
            'email': 'me@johndoe.com',
            'password': 'pass12345',
            'first_name': 'John',
            'last_name': 'Doe'
        }), content_type='application/json', follow_redirects=True)

        self.assert_status(signup_response, 201)

        delete_response = self.client.delete(
            '/api/users/me',
            content_type='application/json',
            follow_redirects=True,
            headers={'Authorization': 'Bearer {}'.format(signup_response.json['app_access_token'])}
        )

        self.assert_status(delete_response, 200)

    def test_update(self):
        signup_response = self.client.post('/signup/email', data=json.dumps({
            'email': 'me@johndoe.com',
            'password': 'pass12345',
            'first_name': 'John',
            'last_name': 'Doe'
        }), content_type='application/json', follow_redirects=True)

        self.assert_status(signup_response, 201)

        update_response = self.client.put(
            '/api/users/me',
            data=json.dumps({
                'first_name': 'Johhny',
                'last_name': 'Doee',
                'email': 'me2@johndoe.com'
            }),
            content_type='application/json',
            follow_redirects=True,
            headers={'Authorization': 'Bearer {}'.format(signup_response.json['app_access_token'])}
        )

        self.assert_status(update_response, 201)

    def test_login(self):
        signup_response = self.client.post('/signup/email', data=json.dumps({
            'email': 'me@johndoe.com',
            'password': 'pass12345',
            'first_name': 'John',
            'last_name': 'Doe'
        }), content_type='application/json', follow_redirects=True)

        self.assert_status(signup_response, 201)

        login_response = self.client.post('/login/email', data=json.dumps({
            'email': 'me@johndoe.com',
            'password': 'pass12345'
        }), content_type='application/json', follow_redirects=True)

        self.assertStatus(login_response, 200)

if __name__ == '__main__':
    unittest.main()
