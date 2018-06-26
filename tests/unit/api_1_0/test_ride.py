"""Contains tests for Ride class."""

import unittest
from app.api_1_0.models import Ride


class TestRide(unittest.TestCase):
    """Test Ride class functionality."""

    def setUp(self):
        """Initialize objects to be used in tests."""
        self.ride = Ride()
        self.ride_data = {"Ride Name": "V8",
                          "Origin": "Thika",
                          "Destination": "Nyeri",
                          "Time": "12:20",
                          "Name": "voyage to meru",
                          "Date": "14-7-2018",
                          "Requests": [],
                          "Id": 1,
                          "Owner": "p@g.com",
                          "Capacity": "12"
        }

    def test_create_ride_with_mandatory_fields_success(self):
        """Test a ride can be created successfuly."""
        res = self.ride.create_ride(self.ride_data)
        self.assertTrue(res)

    def test_create_duplicate_ride_false(self):
        """Test cannot create the same ride twice."""
        self.ride.create_ride(self.ride_data)
        res = self.ride.create_ride(self.ride_data)
        self.assertFalse(res.get('Status'))

    def test_view_ride_if_exist_success(self):
        """Test if a ride can be viewed."""
        self.ride.create_ride(self.ride_data)
        self.assertDictContainsSubset(self.ride_data, self.ride.get_ride("p@g.com", 1).get('Message'))

    def test_view_all_rides_if_exist_success(self):
        """Test if all created rides can be shown."""
        self.ride.create_ride(self.ride_data)
        init_rides = len(self.ride.rides)
        another_ride = {"Ride Name": "V8",
                        "Origin": "Thika",
                        "Destination": "Nyeri",
                        "Time": "8: 30",
                        "Date": "12-7-2018",
                        "Requests": [],
                        "Id": 1,
                        "Owner": "lou@g.com",
                        "Capacity": "6"}
        self.ride.create_ride(another_ride)
        new_rides = len(self.ride.rides)
        self.assertEqual(new_rides, init_rides+1)

    def test_update_ride_if_exist_success(self):
        """Test if a ride can be updated successfuly."""
        res = self.ride.create_ride(self.ride_data)
        self.assertTrue(res)
        update_data = {"Origin": "Nairobi", "Destination": "Naivasha"}
        result = self.ride.edit_ride(1, "p@g.com", update_data)
        self.assertDictContainsSubset(
            update_data, self.ride.get_ride("p@g.com", 1).get('Message'))

    def test_make_ride_request_with_correct_data_success(self):
        """Test a request can be made successfuly."""
        res = self.ride.create_ride(self.ride_data)
        self.assertTrue(res)
        request_data = {"Passenger": "p@g.com", "Ride Owner": "james",
                        "Ride Name": "mwisho wa reli"}
        self.ride.make_request(1, "p@g.com", request_data)
        self.assertCountEqual(self.ride.get_ride("p@g.com", 1).get('Message')['Requests'], [request_data])
