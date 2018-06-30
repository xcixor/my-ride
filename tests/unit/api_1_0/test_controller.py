"""Contains test for the controller."""
import unittest

from app.api_1_0.controller import Controller


class TestController(unittest.TestCase):
    """Test the controller functionality."""

    def setUp(self):
        """Initialize objects for tests."""
        self.controller = Controller()
        self.user_data = {
            "Email": "p@g.com",
            "Password": "pass123",
            "Type": "passenger",
            "Confirm Password": "pass123"
        }
        self.ride_data = {
            "Ride Name": "V8",
            "Origin": "Thika",
            "Destination": "Nyeri",
            "Time": "8: 30",
            "Name": "voyage to meru",
            "Id": 1,
            "Date": "12/7/2018",
            "Requests": [],
            "Owner": "p@g.com",
            "Capacity": "6"
        }

    def test_create_ride_with_incomplete_data_exception_raised(self):
        """Tests exception is raised if ride data contains missing fields."""
        self.assertRaises(Exception, self.controller.create_ride({
            "Name": "Into the badlands",
            "Destination": "Kirinyaga",
            "Time": "7:30"
        }))

    def test_create_user_with_mandatory_fields_success(self):
        """Test create user success."""
        res = self.controller.create_user(self.user_data)
        self.assertEqual(res.get('Message'),
                         'p@g.com Your account has bee Successfuly created')

    def test_login_if_registered_success(self):
        """Test registered user can log in."""
        self.controller.create_user(self.user_data)
        res = self.controller.login(
            {"Email": 'p@g.com', "Password": "pass123"})
        self.assertTrue(res.get('Message'), 'Successfuly Logged in')

    def test_login_if_unregistered_false(self):
        """Test unregistered user cannnot login."""
        res = self.controller.login(
            {"Email": 'p@g.com', "Password": "pass123"})
        self.assertTrue(res.get('Message'), 'Logged in Successfuly')

    def test_create_ride_if_registered_success(self):
        """Test succesful creation of ride for registered user."""
        res = self.controller.create_user(self.user_data)
        self.assertTrue(res.get('Status'))

        result = self.controller.create_ride(self.ride_data)
        self.assertTrue(result.get('Status'))

    def test_create_ride_unregistered_false(self):
        """Test unregistred user is not allowed to create a ride."""
        res = self.controller.create_ride(self.ride_data)
        self.assertEqual(res.get('Message'), 'That user is not registered')

    def test_update_ride_if_registered_success(self):
        """Test successful ride update for registered user."""
        res = self.controller.create_user(self.user_data)
        self.assertTrue(res.get('Status'))

        result = self.controller.create_ride(self.ride_data)
        self.assertTrue(result.get('Status'))

        update_data = {"Vehicle Color": "Red", "Capacity": 7}
        resp = self.controller.edit_ride(1,
            "p@g.com", update_data)
        self.assertTrue(resp.get('Status'))

    def test_get_all_rides_if_exists_success(self):
        """Test all created rides can be retrieved."""
        res = self.controller.create_user(self.user_data)
        self.assertTrue(res.get('Status'))

        result = self.controller.create_ride(self.ride_data)
        self.assertTrue(result.get('Status'))

        resp = self.controller.get_rides()
        self.assertDictContainsSubset(self.ride_data, resp.get(
            'Message').get('p@g.com').get('p@g.com-12/7/2018-8: 30'))

    def test_make_request_if_exists_success(self):
        """Test existing ride can be requested."""
        res = self.controller.create_user(self.user_data)
        self.assertTrue(res.get('Status'))

        result = self.controller.create_ride(self.ride_data)
        self.assertTrue(result.get('Status'))

        resp = self.controller.make_request(1, "p@g.com",
            {"Passenger": "m@y.com",
             "Ride Owner": "james",
             "Ride Name": "mwisho wa reli"})

        self.assertEqual(resp.get('Message'), 'Request made successfuly')