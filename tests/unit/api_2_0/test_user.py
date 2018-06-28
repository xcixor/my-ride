"""Contains tests for user."""
import unittest

import json

from app import create_app


class TestRideModel(unittest.TestCase):
    """Tests the User."""
    def setUp(self):
        """Create app context and initialize db."""
        self.app = create_app('testing')
        self.client = self.app.test_client
        self.app_context = self.app.app_context()
        self.app_context.push()

        self.driver = {
            "Email": "p@gmail.com",
            "Type": "driver",
            "Password": "pass123",
            "Confirm Password": "pass123"
        }

    def tearDown(self):
        """Remove app context, remove db session and delete all records."""
        self.app_context.pop()

    def test_register_user_with_correct_data_success(self):
        """Test a user can be created successfuly."""
        response = self.client().post('/api/v2/auth/register',
                                      data=self.driver)
        result = json.loads(response.data.decode('UTF-8'))
        print('*****************', result)
        self.assertEqual('User created!', result.get('Message'))

    # def test_create_duplicate_user_false(self):
    #     """Test user cannot be registered twice."""
    #     response = self.client().post('/api/v2/auth/register',
    #                                   data=self.driver)
    #     result = json.loads(response.data.decode('UTF-8'))
    #     print('****###################', result)
    #     self.assertEqual('That user already exists', result)

    #     response = self.client().post('/api/v2/auth/register',
    #                                   data=self.driver)
    #     result = json.loads(response.data.decode('UTF-8'))
    #     self.assertFalse(result.get('Status'))

    # def test_login_with_accurate_details_success(self):
    #     """Test Log in successfuly with correct credentials."""
    #     response = self.client().post('/api/v2/auth/register',
    #                                   data=self.driver)
    #     result = json.loads(response.data.decode('UTF-8'))
    #     self.assertDictEqual({'Id': 1, 'Email': 'p@gmail.com',
    #                           'Driver': True}, result.get('Message'))

    #     logins = {'Email': 'p@g.com', 'Password': 'pass123'}

    #     res = self.client().post('/api/v2/auth/login', data=logins)
    #     resp = json.loads(res.data.decode('UTF-8'))
    #     self.assertTrue(resp.get('Status'))

    # def test_user_logout_successs(self):
    #     """Test logged in user can logout successfuly."""
    #     response = self.client().post('/api/v2/auth/register',
    #                                   data=self.driver)
    #     result = json.loads(response.data.decode('UTF-8'))
    #     self.assertDictEqual({'Id': 1, 'Email': 'p@gmail.com',
    #                           'Type': 'Driver'}, result.get('Message'))

    #     logins = {'Email': 'p@g.com', 'Password': 'pass123'}

    #     res = self.client().post('/api/v2/auth/login', data=logins)
    #     resp = json.loads(res.data.decode('UTF-8'))
    #     self.assertTrue(resp.get('Status'))

    #     access_token = resp.get('load').get('token')
    #     result = self.client().post('/api/v2/auth/logout',
    #                                 header= {'Authorization':
    #                                 'Bearer' + access_token})
    #     self.assertEqual('Logout successful', result.get('Message'))

    # def test_generate_token_success(self):
    #     """Test on login user gets a token."""
    #     response = self.client().post('/api/v2/auth/register',
    #                                   data=self.driver)
    #     result = json.loads(response.data.decode('UTF-8'))
    #     self.assertDictEqual({'Id': 1, 'Email': 'p@gmail.com',
    #                           'Driver': True}, result.get('Message'))

    #     logins = {'Email': 'p@g.com', 'Password': 'pass123'}

    #     res = self.client().post('/api/v2/auth/login', data=logins)
    #     resp = json.loads(res.data.decode('UTF-8'))
    #     self.assertTrue(resp.get('Status'))

    #     access_token = resp.get('load').get('token')
    #     self.assertIsNotNone(access_token)
