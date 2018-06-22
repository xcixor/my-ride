"""Contains tests for api endpoints."""
from app.api import views

import unittest


class TestApi (unittest.TestCase):
    """Tests the api endpoints."""

    def setUp(self):
        """Initialize objects for the tests."""
        self.ride = {
                     "Destination": "Meru",
                     "Origin": "Kutus",
                     "Time": "9:00",
                     "Date": "23-6-2018"
                     }

    def tearDown(self):
        """Remove objects after test."""
        del self.ride

    def test_get_all_rides(self):
        """Test get all rides successfuly."""
        pass

    def test_make_ride_request(self):
        """Test user can make a request successfuly."""
        pass

    def test_get_ride(self):
        """Test user can get a ride successfuly."""
        pass

    def test_create_ride(self):
        """Test user can create a ride successfuly."""
        pass

    def test_json_request_only(self):
        """Test the request data is in json format."""
        pass

    def test_required_data_in_request(self):
        """Test request data contains all the necessary fields."""
        pass

    def test_date_data(self):
        """Test date is formatted correctly."""
        pass

    def test_location_in_string(self):
        """Test location data in string format."""
        pass

    def test_request_inexistent_ride(self):
        """Test user is notified if requested ride does not exist."""
        pass

    def test_user_notified_of_ride_request(self):
        """Test a user is notified when the driver accepts or rejects request."""
        pass
