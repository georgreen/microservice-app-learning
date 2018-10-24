import json
import unittest

from project.tests.base import BaseTestCase, db
from project.api.models import User


def add_user(username, email):
    user = User(username=username, email=email)
    db.session.add(user)
    db.session.commit()
    return user


class TestUserService(BaseTestCase):
    """Tests for the Users Service."""

    def test_users(self):
        """Ensure the /ping route behaves correctly."""
        response = self.client.get('/users/ping')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('pong!', data['message'])
        self.assertIn('success', data['status'])

    def test_add_user(self):
        """Ensure users can be added to DB"""
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps(
                    {
                        'username': 'test_user',
                        'email': 'test_user@email.com'
                    }
                ),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('test_user@email.com', data['message'])
            self.assertIn('success', data['status'])

    def test_empty_payload_handled(self):
        """Ensure empty payload is handled"""
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps({}),
                content_type='application/json')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload', data['message'])
            self.assertIn('fail', data['status'])

    def test_invalid_payload_handled(self):
        """Ensure invalid payload is handled"""
        with self.client:
            response = self.client.post(
                '/users', data=json.dumps({
                    'email': 'invalid.email.org'
                }),
                content_type='application/json')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload', data['message'])
            self.assertIn('fail', data['status'])

    def test_duplicate_email_handled(self):
        """Ensure duplicate email payload is handled"""
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps({
                    'email': 'useremail.org@email.com',
                    'username': 'sameuser'
                }),
                content_type='application/json')

            response = self.client.post(
                '/users',
                data=json.dumps({
                    'email': 'useremail.org@email.com',
                    'username': 'sameuser'
                }),
                content_type='application/json')

            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Sorry. That email already exists.', data['message'])
            self.assertIn('fail', data['status'])

    def test_get_single_user(self):
        """Ensure we can get one user."""
        user = add_user(username="testuser", email="testuser@email.com")
        with self.client:
            response = self.client.get(
                f'/users/{user.uid}'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('testuser', data['data']['username'])
            self.assertIn('testuser@email.com', data['data']['email'])
            self.assertIn('success', data['status'])

    def test_get_single_user_404_no_id(self):
        """Ensure 404 for invalid user ids."""
        with self.client:
            response = self.client.get(f'/users/4004')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('User does not exist', data['message'])
            self.assertIn('fail', data['status'])

    def test_get_single_user_404_invalid_id(self):
        """Ensure 404 for invalid user ids."""
        with self.client:
            response = self.client.get(f'/users/noid')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('User does not exist', data['message'])
            self.assertIn('fail', data['status'])

    def test_get_all_users(self):
        """Ensure we can get all users."""
        users = [
            add_user(username="testuser0", email="testuser0@email.com"),
            add_user(username="testuser1", email="testuser1@email.com"),
            add_user(username="testuser2", email="testuser2@email.com")
        ]
        with self.client:
            response = self.client.get(
                '/users'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertTrue(len(data['data']['users']) == len(users))
            self.assertIn('success', data['status'])

    def test_main_no_users(self):
        """Test no users templates is displayed correctly."""
        with self.client:
            response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'All Users', response.data)
        self.assertIn(b'<p>No users!</p>', response.data)

    def test_main_users(self):
        """Test user template is displayed correctly."""
        add_user('testuser1', 'testuser1@email.com')
        add_user('testuser2', 'testuser2@email.com')
        with self.client:
            response = self.client.get('/')
            self.assertEqual(response.status_code, 200)
            self.assertNotIn(b'<p>No users!</p>', response.data)
            self.assertIn(b'testuser1', response.data)
            self.assertIn(b'testuser2', response.data)

    def test_main_add_user(self):
        with self.client:
            response = self.client.post(
                '/',
                data=dict(username='testuser1', email='testuser1@email.com'),
                follow_redirects=True
            )
            self.assertEqual(response.status_code, 200)
            self.assertNotIn(b'<p>No users!</p>', response.data)
            self.assertIn(b'testuser1', response.data)


if __name__ == '__main__':
    unittest.main()
