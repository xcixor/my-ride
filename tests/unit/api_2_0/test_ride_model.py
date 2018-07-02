import unittest

from app.api_2_0.models import Ride


class TestRideModel(unittest.TestCase):

    """Tests the ride model."""

    def setUp(self):
        """Create app context and initialize db."""
        self.ride = Ride()
        self.ride.create_rides_table()
        self.ride = {
            "Ride Name": "V8",
            "Origin": "Thika",
            "Destination": "Nyeri",
            "Time": "8: 30",
            "Date": "12/8/2018",
            "No Plate": "KCE 323 B",
            "Owner Id": 1,
            "Capacity": "6"
        }

    def tearDown(self):
        """Remove app context, remove db session and delete all records."""
        self.ride.drop_rides_table()
        del self.ride

    def test_create_ride_success(self):
        """Test create ride success."""
        res = self.ride.create_ride(self.ride)
        self.assertEqual('Ride created successfully', res.get('Message'))

    def test_get_ride_by_id_success(self):
        """Test ride record can be retrieved from db."""
        res = self.ride.create_ride(self.ride)
        self.assertEqual('Ride created successfully', res.get('Message'))
        resp = self.ride.get_ride_by_id(1)
        self.assertDictContainsSubset(resp.get('Message'), {"Ride Name": "V8"})

    def test_update_ride_success(self):
        """Test ride details can be updated."""
        res = self.ride.create_ride(self.ride)
        self.assertEqual('Ride created successfully', res.get('Message'))
        new_ride = {"No Plate": "KCE 323 B"}
        self.assertDictContainsSubset(self.ride.get_ride_by_id(1), new_ride)

    def test_make_request_success(self):
        """Test ride can be requested successfully."""
        res = self.ride.create_ride(self.ride)
        self.assertEqual('Ride created successfully', res.get('Message'))
        resp = self.ride.request_ride(1, {"User Id": 1})
        self.assertTrue(resp.get('Status'))

    def test_accept_request_success(self):
        res = self.ride.create_ride(self.ride)
        self.assertEqual('Ride created successfully', res.get('Message'))
        resp = self.ride.request_ride(1, {"User Id": 1})
        self.assertTrue(resp.get('Status'))
        res = self.ride.accept_request(1, {"Request Id": 1})
        self.assertTrue(res.get('Status'))

    def test_reject_request_false(self):
        res = self.ride.create_ride(self.ride)
        self.assertEqual('Ride created successfully', res.get('Message'))
        resp = self.ride.request_ride(1, {"User Id": 1})
        self.assertTrue(resp.get('Status'))
        res = self.ride.accept_request(1, {"Request Id": 1})
        self.assertTrue(res.get('Status'))

    def test_get_ride_requests_success(self):
        pass

    def test_get_all_rides_success(self):
        """Test created rides can be retrieved from db."""
        res = self.ride.create_ride(self.ride)
        self.assertEqual('Ride created successfully', res.get('Message'))
        resp = self.ride.request_ride(1, {"User Id": 1})
        self.assertTrue(resp.get('Status'))
        resp = self.ride.request_ride(1, {"User Id": 2})
        self.assertTrue(resp.get('Status'))
        result = self.ride.get_ride_requests(1)
        self.assertCountEqual(result.get('Message'), [1, 2])

    def test_delete_ride_success(self):
        """Test ride can be deleted successfully."""
        res = self.ride.create_ride(self.ride)
        self.assertEqual('Ride created successfully', res.get('Message'))
        self.ride.delete_ride(1)
        self.assertCountEqual(self.ride.get_ride_by_id(1), [])
