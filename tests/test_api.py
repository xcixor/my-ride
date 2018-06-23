"""Contains tests for api endpoints."""

import unittest

from app import create_app


class TestApi(unittest.TestCase):
    """Tests the api endpoints."""

    def setUp(self):
        """Initialize objects for the tests."""
        self.user = {"Email": "p@g.com",
                     "Type": "driver",
                     "Password": "pass123",
                     "Confirm Password": "pass123"}
        self.ride = {"Destination": "Meru",
                     "Origin": "Kutus",
                     "Time": "9:00",
                     "Name": "a ride to meru",
                     "Date": "23-6-2018"}
        self.request = {
            "Passenger Name": "Njobu",
            "Tel": "+254716272376"
        }
        self.app = create_app('testing')
        self.client = self.app.test_client
        self.app.context = self.app.context()
        self.app.context.push()

    def tearDown(self):
        """Remove objects after test."""
        self.app.context.pop()
        del self.ride
        del self.user
        del self.request

    def test_register_user(self):
        """Test user can register successfuly with correct credentials."""
        response = self.client().post('/api/v1/auth/register', data=self.user)
        self.assertEqual(response, 201)

    def test_login(self):
        """Test user can login with correct credentials."""
        response = self.client().post('/api/v1/auth/register', data=self.user)
        self.assertEqual(response, 201)
        logins = {"Email": "p@g.com", "Password": "pass123"}
        res = self.client().post('/api/v1/auth/login', data=logins)
        self.assertTrue(res, 200)

    def test_unregistered_login(self):
        """Test an unregistered user cannot log in."""
        logins = {"email": "p@g.com", "Password": "pass123"}
        res = self.client().post('/api/v1/auth/login', data=logins)
        self.assertTrue(res, 403)

    def test_log_out(self):
        """Test user can logout successfuly."""
        response = self.client().post('api/v1/auth/register', data=self.user)
        self.assertEqual(response, 201)
        logins = {"Email": "p@g.com", "Password": "pass123"}
        res = self.client().post('api/v1/auth/login', data=logins)
        self.assertEqual(res, 200)
        result = self.client().post('api/v1/auth/logout')
        self.assertEqual(result, 200)

    def test_edit_profile(self):
        """Test user can edit their profile."""
        response = self.client().post('api/v1/auth/register', data=self.user)
        self.assertEqual(response, 201)
        logins = {"Email": "p@g.com", "Password": "pass123"}
        res = self.client().post('api/v1/auth/login', data=logins)
        self.assertEqual(res, 200)
        details = {"Email":"p@g.com", "National Id": "34599323",
                   "Vehicle Registration": "KCD E343"}
        result = self.client().put('api/v1/auth/profile', data=details)
        self.assertEqual(result, 200)

    def test_get_user_profile(self):
        """Test user can view their profile."""
        response = self.client().post('api/v1/auth/register', data=self.user)
        self.assertEqual(response, 201)
        logins = {"Email": "p@g.com", "Password": "pass123"}
        res = self.client().post('api/v1/auth/login', data=logins)
        self.assertEqual(res, 200)
        details = {"Email":"p@g.com", "National Id": "34599323",
                   "Tel No": "+254712705422"}
        result = self.client().post('api/v1/auth/profile', data=details)
        self.assertEqual(result, 200)
        result = self.client().get('api/v1/auth/profile')
        self.assertIn('+254712705422', str(result.data))

    def test_create_ride(self):
        """Test user can create a ride successfuly."""
        response = self.client().post('/api/v1/rides', data=self.ride)
        self.assertEqual(response, 201)
        self.assertIn('Meru', str(response.data))

    def test_edit_ride(self):
        """Test user can edit a ride."""
        response = self.client().post('/api/v1/rides', data=self.ride)
        self.assertEqual(response, 201)
        edit_data = {"Vehicle Color": "Red", "Capacity": 7}
        res = self.client().put('/api/v1/rides', data=edit_data)
        self.assertEqual(res.status_code, 200)
        self.assertIn('Red', str(res.data))

    def test_get_ride(self):
        """Test user can get a ride successfuly."""
        response = self.client().post('/api/v1/rides', data=self.ride)
        self.assertEqual(response, 201)
        res = self.client().get('api/v1/rides/1')
        self.assertEqual(res, 200)
        self.assertIn('Meru', str(res.data))

    def test_get_all_rides(self):
        """Test get all rides offers successfuly."""
        response = self.client().post('/api/v1/rides', data=self.ride)
        self.assertEqual(response, 201)
        res = self.client().get('api/v1/rides')
        self.assertEqual(res, 200)
        self.assertIn('Kutus', str(res.data))

    def test_delete_ride(self):
        """Test user can delete ride."""
        response = self.client().post('/api/v1/rides', data=self.ride)
        self.assertEqual(response, 201)
        res = self.client().delete('/api/v1/rides/1')
        self.assertEqual(res, 200)
        result = self.client().get('api/v1/rides/1')
        self.assertEqual(result, 404)

    def test_make_ride_request(self):
        """Test user can make a request successfuly."""
        response = self.client().post('/api/v1/rides', data=self.ride)
        self.assertEqual(response, 201)
        res = self.client().post('api/v1/rides/1/requests', data=self.request)
        self.assertEqual(res, 201)
        self.assertIn('Njobu', str(res.data))

    def test_get_ride_requests(self):
        """Test driver can view a ride's request."""
        response = self.client().post('/api/v1/rides', data=self.ride)
        self.assertEqual(response, 201)
        res = self.client().post('api/v1/rides/1/requests', data=self.request)
        self.assertEqual(res, 201)
        result = self.client().get('api/v1/rides/1/requests')
        self.assertEqual(result, 200)
        self.assertIn(result, '+254716272376')
