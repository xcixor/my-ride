"""Contains tests for api endpoints."""

import unittest
import json
from app import create_app


class TestApi(unittest.TestCase):
    """Tests the api endpoints."""

    def setUp(self):
        """Initialize objects for the tests."""
        self.driver = {
            "Email": "p@gmail.com",
            "Type": "driver",
            "Password": "pass123",
            "Confirm Password": "pass123"
        }
        self.passenger = {
            "Email": "esta@gmail.com",
            "Type": "passenger",
            "Password": "pass234",
            "Confirm Password": "pass234"
        }
        self.ride = {
            "Destination": "Meru",
            "Origin": "Kutus",
            "Time": "9:00",
            # "Name": "a ride to meru",
            "Date": "23-6-2018",
            "Ride Name": "Toyota",
            "Capacity": "7"
        }
        self.request = {
            "Passenger Name": "Njobu",
            "Tel": "+254716272376"
        }
        self.app = create_app('testing')
        self.client = self.app.test_client
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        """Remove objects after test."""
        self.app_context.pop()
        del self.ride
        del self.passenger
        del self.driver
        del self.request

    def test_register_user_with_correct_credentials_success(self):
        """Test user can register successfuly with correct credentials."""
        passenger = {
                "Email": "myi@gmail.com",
                "Type": "passenger",
                "Password": "pass234",
                "Confirm Password": "pass234"
        }
        response = self.client().post('/api/v1/auth/register',
                                      data=passenger)
        self.assertEqual(response.status_code, 201)

    def test_login_with_correct_authentication_success(self):
        """Test user can login with correct credentials."""
        response = self.client().post('/api/v1/auth/register',
                                      data=self.passenger)
        self.assertEqual(response, 201)
        logins = {"Email": "esta@x.com", "Password": "pass234"}
        res = self.client().post('/api/v1/auth/login', data=logins)
        self.assertTrue(res.status_code, 200)

    def test_login_without_registration_false(self):
        """Test an unregistered user cannot log in."""
        logins = {"email": "esta@x.com", "Password": "pass234"}
        res = self.client().post('/api/v1/auth/login', data=logins)
        self.assertTrue(res.status_code, 403)

    def test_logout_sucess(self):
        """Test user can logout successfuly."""
        response = self.client().post('api/v1/auth/register',
                                      data=self.passenger)
        self.assertEqual(response, 201)

        logins = {"Email": "esta@x.com", "Password": "pass234"}
        res = self.client().post('api/v1/auth/login', data=logins)

        self.assertEqual(res, 200)
        result = self.client().post('api/v1/auth/logout')
        self.assertEqual(result, 200)

    def test_edit_profile_if_signed_in_success(self):
        """Test user can edit their profile."""
        response = self.client().post('api/v1/auth/register',
                                      data=self.passenger)
        self.assertEqual(response, 201)
        logins = {"Email": "esta@x.com", "Password": "pass234"}
        res = self.client().post('api/v1/auth/login', data=logins)
        self.assertEqual(res, 200)

        # get authorization token
        token = json.loads(res.data.decode('UTF-8'))
        user_token = token.get('token')

        details = {"Email": "p@g.com", "National Id": "34599323",
                   "Vehicle Registration": "KCD E343"}
        result = self.client().put('api/v1/auth/profile', data=details,
                                   headers={'x-access-token': user_token})
        self.assertEqual(result, 200)

    def test_get_user_profile_if_signed_in_success(self):
        """Test user can view their profile."""
        response = self.client().post('api/v1/auth/register',
                                      data=self.passenger)
        self.assertEqual(response, 201)

        logins = {"Email": "esta@x.com", "Password": "pass234"}
        res = self.client().post('api/v1/auth/login', data=logins)
        self.assertEqual(res, 200)

        # get authorization token
        token = json.loads(res.data.decode('UTF-8'))
        user_token = token.get('token')

        details = {"Email": "estaz@g.com", "National Id": "34599323",
                   "Tel No": "+254712705422"}
        result = self.client().post('api/v1/auth/profile', data=details,
                                    headers={'x-access-token': user_token})
        self.assertEqual(result, 200)

        result = self.client().get('api/v1/auth/profile',
                                   headers={'x-access-token': user_token})
        self.assertIn('+254712705422', str(result.data))

    def test_create_ride_if_signed_in_success(self):
        """Test user can create a ride successfuly."""
        # signup
        response = self.client().post('api/v1/auth/register',
                                      data=self.driver)
        self.assertEqual(response.status_code, 201)

        # login
        logins = {"Email": "p@gmail.com", "Password": "pass123"}
        res = self.client().post('api/v1/auth/login', data=logins)
        self.assertEqual(res.status_code, 201)

        response = self.client().post('/api/v1/rides', data=self.ride)
        self.assertEqual(response.status_code, 201)
        self.assertIn('Meru', str(response.data))

    def test_edit_ride_if_signed_in_success(self):
        """Test user can edit a ride."""
        # signup
        response = self.client().post('api/v1/auth/register',
                                      data=self.driver)
        self.assertEqual(response, 201)

        # login
        logins = {"Email": "p@g.com", "Password": "pass123"}
        res = self.client().post('api/v1/auth/login', data=logins)
        self.assertEqual(res, 200)

        # get authorization token
        token = json.loads(res.data.decode('UTF-8'))
        user_token = token.get('token')

        # create ride
        response = self.client().post('/api/v1/rides', data=self.ride,
                                      headers={'x-access-token': user_token})
        self.assertEqual(response, 201)

        # edit the ride
        edit_data = {"Vehicle Color": "Red", "Capacity": 7}
        res = self.client().put('/api/v1/rides', data=edit_data,
                                headers={'x-access-token': user_token})
        self.assertEqual(res.status_code, 200)
        self.assertIn('Red', str(res.data))

    def test_get_ride_if_exists_success(self):
        """Test user can get a ride successfuly."""
        response = self.client().post('/api/v1/rides', data=self.ride)
        self.assertEqual(response, 201)
        res = self.client().get('api/v1/rides/1')
        self.assertEqual(res, 200)
        self.assertIn('Meru', str(res.data))

    def test_get_all_rides_if_exists_success(self):
        """Test get all rides offers successfuly."""
        response = self.client().post('/api/v1/rides', data=self.ride)
        self.assertEqual(response, 201)
        res = self.client().get('api/v1/rides')
        self.assertEqual(res, 200)
        self.assertIn('Kutus', str(res.data))

    def test_delete_ride_if_signed_in_success(self):
        """Test user can delete ride."""
        # signup
        response = self.client().post('api/v1/auth/register',
                                      data=self.driver)
        self.assertEqual(response, 201)

        # login
        logins = {"Email": "p@g.com", "Password": "pass123"}
        res = self.client().post('api/v1/auth/login', data=logins)
        self.assertEqual(res, 200)

        # get authorization token
        token = json.loads(res.data.decode('UTF-8'))
        user_token = token.get('token')

        # creat ride
        response = self.client().post('/api/v1/rides', data=self.ride,
                                      headers={'x-access-token': user_token})
        self.assertEqual(response, 201)

        # delete ride
        res = self.client().delete('/api/v1/rides/1',
                                   headers={'x-access-token': user_token})
        self.assertEqual(res, 200)
        result = self.client().get('api/v1/rides/1')
        self.assertEqual(result, 404)

    def test_make_ride_request_if_signed_in_success(self):
        """Test user can make a request successfuly."""
        # signup
        response = self.client().post('api/v1/auth/register',
                                      data=self.driver)
        self.assertEqual(response, 201)

        # login
        logins = {"Email": "p@g.com", "Password": "pass234"}
        res = self.client().post('api/v1/auth/login', data=logins)
        self.assertEqual(res, 200)

        # get authorization token
        token = json.loads(res.data.decode('UTF-8'))
        user_token = token.get('token')

        response = self.client().post('/api/v1/rides', data=self.ride)
        self.assertEqual(response, 201)

        res = self.client().post('api/v1/rides/1/requests', data=self.request,
                                 headers={'x-access-token': user_token})
        self.assertEqual(res, 201)
        self.assertIn('Njobu', str(res.data))

    def test_get_ride_requests_if_signed_in_success(self):
        """Test driver can view a ride's request."""
        # signup
        response = self.client().post('api/v1/auth/register',
                                      data=self.driver)
        self.assertEqual(response, 201)

        # login
        logins = {"Email": "p@g.com", "Password": "pass234"}
        res = self.client().post('api/v1/auth/login', data=logins)
        self.assertEqual(res, 200)

        # get authorization token
        token = json.loads(res.data.decode('UTF-8'))
        user_token = token.get('token')

        response = self.client().post('/api/v1/rides', data=self.ride,
                                      headers={'x-access-token': user_token})
        self.assertEqual(response, 201)

        res = self.client().post('api/v1/rides/1/requests', data=self.request,
                                 headers={'x-access-token': user_token})
        self.assertEqual(res, 201)

        result = self.client().get('api/v1/rides/1/requests',
                                   headers={'x-access-token': user_token})
        self.assertEqual(result, 200)
        self.assertIn(result, '+254716272376')
