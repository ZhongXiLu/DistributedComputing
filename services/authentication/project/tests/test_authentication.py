import json
import unittest

from project import db
from project.api.models import Password
from project.tests.base import BaseTestCase


def add_password(user_id, password):
    pw = Password(user_id=user_id, password=password)
    db.session.add(pw)
    db.session.commit()
    return pw


class TestUserService(BaseTestCase):
    """Tests for the Users Service."""

    def test_users(self):
        """Ensure the /ping route behaves correctly."""
        response = self.client.get('/ping')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('pong!', data['message'])
        self.assertIn('success', data['status'])

    def test_add_password(self):
        """Ensure a new password can be added to the database."""
        with self.client:
            response = self.client.post(
                '/passwords',
                data=json.dumps({
                    'user_id': 0,
                    'password': 'correct horse battery staple'
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('0\'s password was added!', data['message'])
            self.assertIn('success', data['status'])

    def test_add_password_invalid_json(self):
        """Ensure error is thrown if the JSON object is empty."""
        with self.client:
            response = self.client.post(
                '/passwords',
                data=json.dumps({}),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_password_invalid_json_keys(self):
        """
        Ensure error is thrown if the JSON object does not have a valid user_id or password key.
        """
        invalid_jsons = [
            {'password': '7kbe9d'},  # user_id must not be None
            {'user_id': 0},  # password must not be None
            {'user_id': 0.0, 'password': '6bjvpe'},  # user_id must be integer
            {'user_id': '0.0', 'password': '6bjvpe'},  # user_id must be integer
        ]
        for invalid_json in invalid_jsons:
            response = self.client.post(
                '/passwords',
                data=json.dumps(invalid_json),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_password_duplicate_user_id(self):
        """Ensure error is thrown if the user_id already exists."""
        with self.client:
            # add_password(0, 'ozlq6qwm')
            self.client.post(
                '/passwords',
                data=json.dumps({
                    'user_id': 0,
                    'password': 'ozlq6qwm'
                }),
                content_type='application/json',
            )
            response = self.client.post(
                '/passwords',
                data=json.dumps({
                    'user_id': 0,
                    'password': 'ozlq6qwm_2'
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn(f'User 0 already exists.', data['message'])
            self.assertIn('fail', data['status'])

    def test_validate_password(self):
        """Ensure right response when providing no password"""
        with self.client:
            add_password(0, "asdf")

            response = self.client.get(
                '/verify_credentials'
            )
            self.assert401(response)

            # self.client.get()

    '''
    def test_single_user(self):
        """Ensure get single user behaves correctly."""
        user = add_user('michael', 'michael@mherman.org')
        with self.client:
            response = self.client.get(f'/users/{user.id}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('michael', data['data']['username'])
            self.assertIn('michael@mherman.org', data['data']['email'])
            self.assertIn('success', data['status'])

    def test_single_user_no_id(self):
        """Ensure error is thrown if an id is not provided."""
        with self.client:
            response = self.client.get('/users/blah')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('User does not exist', data['message'])
            self.assertIn('fail', data['status'])

    def test_single_user_incorrect_id(self):
        """Ensure error is thrown if the id does not exist."""
        with self.client:
            response = self.client.get('/users/999')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('User does not exist', data['message'])
            self.assertIn('fail', data['status'])

    def test_all_users(self):
        """Ensure get all users behaves correctly."""
        add_user('michael', 'michael@mherman.org')
        add_user('fletcher', 'fletcher@notreal.com')
        with self.client:
            response = self.client.get('/users')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['users']), 2)
            self.assertIn('michael', data['data']['users'][0]['username'])
            self.assertIn('michael@mherman.org', data['data']['users'][0]['email'])
            self.assertIn('fletcher', data['data']['users'][1]['username'])
            self.assertIn('fletcher@notreal.com', data['data']['users'][1]['email'])
            self.assertIn('success', data['status'])

    def test_all_users_empty(self):
        """Ensure get all users behaves correctly when there are no users."""
        with self.client:
            response = self.client.get('/users')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['users']), 0)
            self.assertIn('success', data['status'])

    '''


if __name__ == '__main__':
    unittest.main()
