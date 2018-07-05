"""Contains tests for user."""
import unittest

import json

from app import create_app

from app.api_2_0.controller import Controller


class TestUserEndpoints(unittest.TestCase):
    """Tests the User."""
    def setUp(self):
        """Create app context and initialize db."""
        self.app = create_app('testing')
        self.client = self.app.test_client
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.db = Controller()
        self.db.create_all()

        self.driver = {
            "Email": "p@gmail.com",
            "Type": "driver",
            "Password": "pass123",
            "Confirm Password": "pass123"
        }

    def tearDown(self):
        """Remove app context, remove db session and delete all records."""
        self.app_context.pop()
        self.db.drop_all()

    def test_register_user_with_correct_data_success(self):
        """Test a user can be created successfuly."""
        response = self.client().post('/api/v2/auth/register',
                                      data=self.driver)
        result = json.loads(response.data.decode('UTF-8'))
        self.assertEqual('Succesfuly created user record',
                         result.get('Message'))

    def test_create_duplicate_user_false(self):
        """Test user cannot be registered twice."""
        response = self.client().post('/api/v2/auth/register',
                                      data=self.driver)
        result = json.loads(response.data.decode('UTF-8'))
        self.assertEqual(result.get('Message'), \
                                    'Succesfuly created user record')

        response = self.client().post('/api/v2/auth/register',
                                      data=self.driver)
        result = json.loads(response.data.decode('UTF-8'))
        self.assertFalse(result.get('Status'))

    def test_login_with_accurate_details_success(self):
        """Test Log in successfuly with correct credentials."""
        response = self.client().post('/api/v2/auth/register',
                                      data=self.driver)
        self.assertEqual(201, response.status_code)

        logins = {'Email': 'p@gmail.com', 'Password': 'pass123'}

        res = self.client().post('/api/v2/auth/login', data=logins)
        self.assertEqual(200, res.status_code)

    def test_generate_token_success(self):
        """Test on login user gets a token."""
        response = self.client().post('/api/v2/auth/register',
                                      data=self.driver)
        result = json.loads(response.data.decode('UTF-8'))
        self.assertEqual(result.get('Message'),
                         'Succesfuly created user record')

        logins = {'Email': 'p@gmail.com', 'Password': 'pass123'}

        res = self.client().post('/api/v2/auth/login', data=logins)
        self.assertEqual(200, res.status_code)

        resp = json.loads(res.data.decode('UTF-8'))
        access_token = resp.get('access-token')
        self.assertIsNotNone(access_token)
