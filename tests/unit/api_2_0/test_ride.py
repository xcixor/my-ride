"""Contains tests for ride endpoints."""
import unittest

import json

from app import create_app, DB


class TestRideEndpoints(unittest.TestCase):
    """Tests the Ride."""

    def setUp(self):
        """Create app context and initialize db."""
        self.app = create_app('testing')
        self.client = self.app.test_client
        self.app_context = self.app.app_context()
        self.app_context.push()
        DB.create_all()

        self.driver = {
            "Email": "p@gmail.com",
            "Type": "driver",
            "Password": "pass123",
            "Confirm Password": "pass123"
        }
        self.ride = {
            "Destination": "Meru",
            "Origin": "Kutus",
            "Time": "9:00",
            "Date": "23-6-2018",
            "Ride Name": "Toyota",
            "Capacity": "7"
        }
        self.request = {
            "Email": "dush@yahoo.com"
        }

    def tearDown(self):
        """Remove app context, remove db session and delete all records."""
        self.app_context.pop()
        DB.session.remove()
        DB.drop_all()

    def test_create_ride_success(self):
        """Test a ride can be created successfully with the right data."""
        response = self.client().post('/api/v2/auth/register',
                                              data=self.driver)
        result = json.load(response.data.decode('UTF-8'))
        self.assertDictEqual({'Id': 1, 'Email': 'p@gmail.com',
                              'Driver': True}, result.get('Message'))

        logins = {'Email': 'p@g.com', 'Password': 'pass123'}

        res = self.client().post('/api/v2/auth/login', data=logins)
        resp = json.loads(res.data.decode('UTF-8'))
        self.assertTrue(resp.get('Status'))

        access_token = resp.get('load').get('token')

        response = self.client().post('/api/v2/rides', data=self.ride,
                                      headers={'Authorization':
                                      'Bearer '+access_token})
        data = json.loads(response.data.decode('utf-8'))
        self.assertTrue(data.get('success'))

    def create_ride(self):
        """Create ride to use for subsequent tests."""
        response = self.client().post('/api/v2/auth/register',
                                      data=self.driver)

        logins = {'Email': 'p@g.com', 'Password': 'pass123'}

        res = self.client().post('/api/v2/auth/login', data=logins)
        resp = json.loads(res.data.decode('UTF-8'))

        access_token = resp.get('load').get('token')

        response = self.client().post('/api/v2/user/rides', data=self.ride,
                                      headers={'Authorization':
                                               'Bearer '+access_token})
        ride_data = json.loads(response.data.decode('utf-8'))

        return {'token': access_token, 'ride': ride_data}

    def test_get_existing_rides_success(self):
        """Test user can get a ride."""
        self.create_ride()

        resp = self.client().post('/api/v2/rides')
        resp_data = json.loads(resp.data.decode('UTF-8'))
        self.assertTrue(resp_data.get('Status'))

    def test_get_inexisting_rides_false(self):
        resp = self.client().post('/api/v2/rides')
        resp_data = json.loads(resp.data.decode('UTF-8'))
        self.assertFalse(resp_data.get('Status'))

    def test_get_single_ride_if_exist_success(self):
        """Test retrieve a single ride with id."""
        data = self.create_ride()
        access_token = data.get('token')

        resp = self.client().post('/api/v2/rides/1',
                                  headers={'Authorization':
                                           'Bearer '+access_token})
        resp_data = json.loads(resp.data.decode('UTF-8'))
        self.assertIn('Meru', resp_data.get('Message'))

    def test_edit_ride_success(self):
        """Test a ride can be edited successfully."""
        data = self.create_ride()
        access_token = data.get('token')

        edit_data = {'Destination': 'Kiawara', 'Origin': 'Gutee'}
        resp = self.client().put('/api/v2/rides/1', data=edit_data,
                                 headers={'Authorization':
                                          'Bearer '+access_token})
        resp_data = json.loads(resp.data.decode('UTF-8'))
        self.assertTrue(resp_data.get('Status'))

    def test_request_ride_success(self):
        """Test user can request ride."""
        data = self.create_ride()
        ride_id = data.get('ride').get('Id')
        resp = self.client().put('/api/v2/rides/{}/requests'.format(ride_id),
                                 data=self.request)
        resp_data = json.loads(resp.data.decode('UTF-8'))
        self.assertEqual('Request made successfully', resp_data.get('Message'))

    def test_accept_request_success(self):
        """Test driver can accept a reques."""
        data = self.create_ride()
        access_token = data.get('token')
        ride_id = data.get('ride').get('Id')
        resp = self.client().put('/api/v2/rides/{}/requests'.format(ride_id),
                                 data=self.request)
        resp_data = json.loads(resp.data.decode('UTF-8'))
        self.assertEqual('Request made successfully', resp_data.get('Message'))

        resp = self.client().post('/api/v2/user/rides/{}/\
                                  requests/1'.format(ride_id),
                                  data={'email': 'dush@yahoo.com',
                                  'status': True},
                                  headers={'Authorization':
                                           'Bearer '+access_token})
        resp_data = json.loads(resp.data.decode('UTF-8'))
        self.assertEqual('Request Accepted', resp_data.get('Message'))

    def test_reject_request_success(self):
        """Test driver can accept a request."""
        data = self.create_ride()
        access_token = data.get('token')
        ride_id = data.get('ride').get('Id')
        resp = self.client().put('/api/v2/rides/{}/requests'.format(ride_id),
                                 data=self.request)
        resp_data = json.loads(resp.data.decode('UTF-8'))
        self.assertEqual('Request made successfully', resp_data.get('Message'))

        resp = self.client().post('/api/v2/user/rides/{}/\
                                  requests/1'.format(ride_id),
                                  data={'email': 'dush@yahoo.com',
                                        'status': False},
                                  headers={'Authorization':
                                           'Bearer '+access_token})
        resp_data = json.loads(resp.data.decode('UTF-8'))
        self.assertEqual('Request Rejected', resp_data.get('Message'))

    def get_ride_requests_success(self):
        data = self.create_ride()
        access_token = data.get('token')
        ride_id = data.get('ride').get('Id')
        resp = self.client().put('/api/v2/rides/{}/requests'.format(ride_id),
                                 data=self.request)
        resp_data = json.loads(resp.data.decode('UTF-8'))
        self.assertEqual('Request made successfully', resp_data.get('Message'))

        res = self.client().post('/api/v2/user/rides/{}/\
                                 requests'.format(ride_id),
                                 headers={'Authorization':
                                          'Bearer '+access_token})
        res_data = json.loads(resp.data.decode('UTF-8'))
        self.assertTrue(res_data.get('Status'))
