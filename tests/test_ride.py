"""Contains tests for Ride class."""

import unittest
from app.api_1_0.models import Ride


class TestRide(unittest.TestCase):
    """Test Ride class functionality."""

    def setUp(self):
        """Initialize objects to be used in tests."""
        self.ride = Ride()
        self.ride_data = {"Origin": "Thika",
                          "Destination": "Nyeri",
                          "Departure": "8: 30",
                          "Name": "voyage to meru",
                          "Date": "12-7-2018"}

    def test_create_ride(self):
        """Test a ride can be created successfuly."""
        res = self.ride.create_ride(self.ride_data)
        self.assertTrue(res)

    def test_create_duplicate_ride(self):
        """Test cannot create the same ride twice."""
        self.ride.create_ride(self.ride_data)
        res = self.ride.create_ride(self.ride_data)
        self.assertFalse(res)

    def test_view_ride(self):
        """Test if a ride can be viewed."""
        self.ride.create_ride(self.ride_data)
        self.assertDictContainsSubset(self.ride_data, self.ride.get_ride(1))

    def test_view_all_rides(self):
        """Test if all created rides can be shown."""
        self.ride.create_ride(self.ride_data)
        init_rides = len(self.ride.rides)
        another_ride = {"Origin": "Nairobi",
                        "Destination": "Nyahururu",
                        "Departure": "8: 30",
                        "Name": "mwisho wa reli",
                        "Date": "12-7-2018"}
        self.ride.create_ride(another_ride)
        new_rides = self.ride.rides
        self.assertEqual(init_rides, new_rides+1)

    def test_update_ride(self):
        """Test if a ride can be updated successfuly."""
        res = self.ride.create_ride(self.ride_data)
        self.assertTrue(res)
        update_data = {"Vehicle Color": "Red", "Capacity": 7}
        self.ride.update_ride(update_data)
        self.assertDictContainsSubset(update_data, self.ride.get_ride(1))

    def test_delete_ride(self):
        """Test ride can be deleted successfuly."""
        res = self.ride.create_ride(self.ride_data)
        self.assertTrue(res)
        result = self.ride.delete_ride(1)
        self.assertTrue(result)
        self.assertFalse(self.ride.get_ride('mwisho wa reli'))

    def test_make_ride_request(self):
        """Test a request can be made successfuly."""
        res = self.ride.create_ride(self.ride_data)
        self.assertTrue(res)
        request_data = {"User": "p@g.com", "Ride Owner": "james",
                        "Ride Name": "mwisho wa reli"}
        self.ride.request_ride(request_data)
        self.assertCountEqual(self.ride.get_ride(1)['requests'],
                              [{"User": "p@g.com", "Ride Owner": "james",
                                "Ride Name": "mwisho wa reli"}])

    def test_get_ride_requests(self):
        """Test ride requests can be retrieved."""
        res = self.ride.create_ride(self.ride_data)
        self.assertTrue(res)
        request_data = {"User": "p@g.com", "Ride Owner": "james",
                        "Ride Name": "mwisho wa reli"}
        self.ride.request_ride(request_data)
        init_len = len(self.ride.get_requests('mwisho wa reli', 'james'))
        request_data = {"User": "m@y.com", "Ride Owner": "james",
                        "Ride Name": "mwisho wa reli"}
        self.ride.request_ride(request_data)
        new_len = len(self.ride.get_requests('mwisho wa reli', 'james'))
        self.assertEqual(init_len+1, new_len)
