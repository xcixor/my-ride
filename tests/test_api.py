"""Contains tests for api endpoints."""

import unittest

from app import create_app


class TestApi(unittest.TestCase):
    """Tests the api endpoints."""

    def setUp(self):
        """Initialize objects for the tests."""
        self.ride = {"Destination": "Meru",
                     "Origin": "Kutus",
                     "Time": "9:00",
                     "Date": "23-6-2018"}
        self.request = {
            "Passenger Name": "Njobu",
            "Tel": "+254716272376"
        }
        self.app = create_app('testing')
        self.client = self.app.test_client
        self.app.context.push()

    def tearDown(self):
        """Remove objects after test."""
        self.app.context.pop()
        del self.ride

    def test_create_ride(self):
        """Test user can create a ride successfuly."""
        response = self.client().post('/api/v1/rides', data=self.ride)
        self.assertEqual(response, 201)
        self.assertIn('Meru', str(response.data))

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
