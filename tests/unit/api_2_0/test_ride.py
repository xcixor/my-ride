"""Contains tests for ride endpoints."""
import unittest

import json

from app import create_app


from app.api_2_0.controller import Controller


class TestRideEndpoints(unittest.TestCase):
    """Tests the Ride."""

    def setUp(self):
        """Create app context and initialize db."""
        self.app = create_app('testing')
        self.controller = Controller()
        self.controller.create_all()
        self.client = self.app.test_client
        self.app_context = self.app.app_context()
        self.app_context.push()

        self.driver = {
            "Email": "p@gmail.com",
            "Type": "driver",
            "Password": "pass123",
            "Confirm Password": "pass123"
        }
        self.passenger = {
            "Email": "p@g.com",
            "Type": "driver",
            "Password": "pass123",
            "Confirm Password": "pass123"
        }
        self.ride = {
            "Destination": "Meru",
            "Origin": "Kutus",
            "Time": "11:00",
            "Date": "23/9/2018",
            "Ride Name": "Toyota",
            "Capacity": 7,
            "Owner": "p@gmail.com",
            "No Plate": "KCE"
        }

    def tearDown(self):
        """Remove app context, remove db session and delete all records."""
        self.app_context.pop()
        self.controller.drop_all()

    def test_create_ride_success(self):
        """Test a ride can be created successfully with the right data."""
        response = self.client().post('/api/v2/auth/register',
                                              data=self.driver)
        self.assertEqual(201, response.status_code)

        logins = {'Email': 'p@gmail.com', 'Password': 'pass123'}

        res = self.client().post('/api/v2/auth/login', data=logins)
        self.assertEqual(200, res.status_code)

        resp = json.loads(res.data.decode('UTF-8'))
        access_token = resp.get('access-token')

        response = self.client().post('/api/v2/rides', data=self.ride,
                                      headers={'Authorization':
                                      'Bearer '+access_token})
        self.assertEqual(201, response.status_code)

    # def create_ride(self):
    #     """Create ride to use for subsequent tests."""
    #     response = self.client().post('/api/v2/auth/register',
    #                                   data=self.driver)

    #     logins = {'Email': 'p@gmail.com', 'Password': 'pass123'}

    #     res = self.client().post('/api/v2/auth/login', data=logins)
    #     resp = json.loads(res.data.decode('UTF-8'))

    #     access_token = resp.get('access-token')

    #     response = self.client().post('/api/v2/rides', data=self.ride,
    #                                   headers={'Authorization':
    #                                            'Bearer '+access_token})
    #     ride_data = json.loads(response.data.decode('utf-8'))
    #     print(ride_data,'******************************')
    #     ride = self.client().post('/api/v2/ride', headers={'Authorization':
    #                                                        'Bearer '+access_token})
    #     print(ride)
    #     return {'token': access_token, 'ride': ride_data}

    def test_get_existing_rides_success(self):
        """Test user can get a ride."""
        response = self.client().post('/api/v2/auth/register',
                                              data=self.driver)
        self.assertEqual(201, response.status_code)

        logins = {'Email': 'p@gmail.com', 'Password': 'pass123'}

        res = self.client().post('/api/v2/auth/login', data=logins)
        self.assertEqual(200, res.status_code)

        resp = json.loads(res.data.decode('UTF-8'))
        access_token = resp.get('access-token')

        response = self.client().post('/api/v2/rides', data=self.ride,
                                      headers={'Authorization':
                                               'Bearer '+access_token})
        self.assertEqual(201, response.status_code)
        result = self.client().get('api/v2/rides', headers={'Authorization':
                                                            'Bearer '+access_token})
        result = self.client().get('api/v2/rides', headers={'Authorization':
                                                   'Bearer '+access_token})
        self.assertEqual(200, result.status_code)


    def test_get_inexisting_rides_false(self):
        resp = self.client().post('/api/v2/rides')
        self.assertEqual(401, resp.status_code)

    def test_get_single_ride_if_exist_success(self):
        """Test retrieve a single ride with id."""
        response = self.client().post('/api/v2/auth/register',
                                              data=self.driver)
        self.assertEqual(201, response.status_code)

        logins = {'Email': 'p@gmail.com', 'Password': 'pass123'}

        res = self.client().post('/api/v2/auth/login', data=logins)
        self.assertEqual(200, res.status_code)

        resp = json.loads(res.data.decode('UTF-8'))
        access_token = resp.get('access-token')

        response = self.client().post('/api/v2/rides', data=self.ride,
                                      headers={'Authorization':
                                               'Bearer '+access_token})
        self.assertEqual(201, response.status_code)

        result = self.client().get('/api/v2/rides/1', headers={'Authorization': 'Bearer '+access_token})
        self.assertEqual(200, result.status_code)

    def test_request_ride_success(self):
        """Test user can request ride."""
        response = self.client().post('/api/v2/auth/register',
                                              data=self.driver)
        self.assertEqual(201, response.status_code)

        logins = {'Email': 'p@gmail.com', 'Password': 'pass123'}

        res = self.client().post('/api/v2/auth/login', data=logins)
        self.assertEqual(200, res.status_code)

        resp = json.loads(res.data.decode('UTF-8'))
        access_token = resp.get('access-token')

        response = self.client().post('/api/v2/rides', data=self.ride,
                                      headers={'Authorization':
                                               'Bearer '+access_token})

        # create passenger
        self.assertEqual(201, response.status_code)
        response = self.client().post('/api/v2/auth/register',
                                      data=self.passenger)
        self.assertEqual(201, response.status_code)

        logins = {'Email': 'p@g.com', 'Password': 'pass123'}

        res = self.client().post('/api/v2/auth/login', data=logins)
        self.assertEqual(200, res.status_code)

        resp = json.loads(res.data.decode('UTF-8'))
        pass_token = resp.get('access-token')

        resp = self.client().post('/api/v2/rides/1/requests',
                                  headers={'Authorization':
                                           'Bearer '+pass_token})
        self.assertEqual(201, resp.status_code)

    # def test_accept_request_success(self):
    #     """Test driver can accept a reques."""
    #     data = self.create_ride()
    #     access_token = data.get('token')
    #     ride_id = data.get('ride').get('Id')
    #     resp = self.client().put('/api/v2/rides/{}/requests'.format(ride_id),
    #                              data=self.request)
    #     resp_data = json.loads(resp.data.decode('UTF-8'))
    #     self.assertEqual('Request made successfully', resp_data.get('Message'))

    #     resp = self.client().post('/api/v2/user/rides/{}/\
    #                               requests/1'.format(ride_id),
    #                               data={'email': 'dush@yahoo.com',
    #                               'status': True},
    #                               headers={'Authorization':
    #                                        'Bearer '+access_token})
    #     resp_data = json.loads(resp.data.decode('UTF-8'))
    #     self.assertEqual('Request Accepted', resp_data.get('Message'))

    # def test_reject_request_success(self):
    #     """Test driver can accept a request."""
    #     data = self.create_ride()
    #     access_token = data.get('token')
    #     ride_id = data.get('ride').get('Id')
    #     resp = self.client().put('/api/v2/rides/{}/requests'.format(ride_id),
    #                              data=self.request)
    #     resp_data = json.loads(resp.data.decode('UTF-8'))
    #     self.assertEqual('Request made successfully', resp_data.get('Message'))

    #     resp = self.client().post('/api/v2/user/rides/{}/\
    #                               requests/1'.format(ride_id),
    #                               data={'email': 'dush@yahoo.com',
    #                                     'status': False},
    #                               headers={'Authorization':
    #                                        'Bearer '+access_token})
    #     resp_data = json.loads(resp.data.decode('UTF-8'))
    #     self.assertEqual('Request Rejected', resp_data.get('Message'))

    def test_get_ride_requests_success(self):
        """Create driver."""
        user_response = self.client().post('/api/v2/auth/register',
                                      data=self.driver)
        self.assertEqual(201, user_response.status_code)

        # login driver to create ride
        logins = {'Email': 'p@gmail.com', 'Password': 'pass123'}
        res = self.client().post('/api/v2/auth/login', data=logins)
        self.assertEqual(200, res.status_code)

        # get token
        resp = json.loads(res.data.decode('UTF-8'))
        access_token = resp.get('access-token')

        # create ride
        response = self.client().post('/api/v2/rides', data=self.ride,
                                      headers={'Authorization':
                                               'Bearer '+access_token})

        # create passenger
        self.assertEqual(201, response.status_code)
        response = self.client().post('/api/v2/auth/register',
                                      data=self.passenger)
        self.assertEqual(201, response.status_code)

        # login passenger
        logins = {'Email': 'p@g.com', 'Password': 'pass123'}
        login_res = self.client().post('/api/v2/auth/login', data=logins)
        self.assertEqual(200, login_res.status_code)

        # get token
        login_resp = json.loads(login_res.data.decode('UTF-8'))
        pass_token = login_resp.get('access-token')

        # make request
        ride_resp = self.client().post('/api/v2/rides/1/requests',
                                  headers={'Authorization':
                                           'Bearer '+pass_token})
        ride_response = json.loads(ride_resp.data.decode('UTF-*'))
        self.assertEqual(201, ride_resp.status_code)

        # get requests
        requests = self.client().get('/api/v2/users/rides/1/requests',
                                     headers={'Authorization': \
                                              'Bearer '+access_token})
        self.assertEqual(requests.status_code, 200)
