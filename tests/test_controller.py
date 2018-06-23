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
            "Confirm Password": "pass123"
        }
        self.ride_data = {
            "Origin": "Thika",
            "Destination": "Nyeri",
            "Departure": "8: 30",
            "Name": "voyage to meru",
            "Date": "12-7-2018",
            "Requests": [],
            "Ride Owner": "p@g.com"
        }

    def test_cannot_create_ride_with_incomplete_data(self):
        """Tests exception is raised if ride data contains missing fields."""
        self.assertRaises(Exception, self.controller.create_ride({
                "Name": "Into the badlands",
                "Destination": "Kirinyaga",
                "Time": "7:30",
            }))

    def test_create_user(self):
        """Test create user success."""
        res = self.controller.create_user(self.user_data)
        self.assertEqual(res.get('message'), 'User created successfuly')

    def test_login(self):
        """Test registered user can log in."""
        self.controller.create_user(self.user_data)
        res = self.controller.login(
            {"Email": 'p@g.com', "Password": "pass123"})
        self.assertTrue(res.get('message'), 'Successfuly Logged in')

    def test_unregistered_user_login(self):
        """Test unregistered user cannnot login."""
        res = self.controller.login(
            {"Email": 'p@g.com', "Password": "pass123"})
        self.assertTrue(res.get('message'), 'Logged in Successfuly')

    def test_create_ride(self):
        """Test succesful creation of ride for registered user."""
        res = self.controller.create_user(self.user_data)
        self.assertTrue(res.get('status'))

        result = self.controller.create_ride(self.ride_data)
        self.assertEqual(result.get('message'), 'Ride created successfuly')

    def test_unregistered_user_cannot_create_ride(self):
        """Test unregistred user is not allowed to create a ride."""
        res = self.controller.create_ride(self.ride_data)
        self.assertEqual(res.get('message'), 'That user does not exist')

    def test_update_ride(self):
        """Test successful ride update for registered user."""
        res = self.controller.create_user(self.user_data)
        self.assertTrue(res.get('status'))

        result = self.controller.create_ride(self.ride_data)
        self.assertTrue(result.get('status'))

        update_data = {"Vehicle Color": "Red", "Capacity": 7}
        resp = self.controller.update_ride(
            "p@g.com", "voyage to meru", update_data)
        self.assertEqual(resp.get('message'), "Ride update Successfuly")

    def test_get_user_rides(self):
        """Test rides for registed user can be retrieved."""
        res = self.controller.create_user(self.user_data)
        self.assertTrue(res.get('status'))

        result = self.controller.create_ride(self.ride_data)
        self.assertTrue(result.get('status'))

        resp = self.controller.get_user_rides("p@g.com")
        self.assertDictContainsSubset(resp.get('message'), self.ride_data)

    def test_get_all_rides(self):
        """Test all created rides can be retrieved."""
        res = self.controller.create_user(self.user_data)
        self.assertTrue(res.get('status'))

        result = self.controller.create_ride(self.ride_data)
        self.assertTrue(result.get('status'))

        resp = self.controller.get_all_rides()
        self.assertDictContainsSubset(resp.get('message'), self.ride_data)

    def test_make_request(self):
        """Test existing ride can be requested."""
        res = self.controller.create_user(self.user_data)
        self.assertTrue(res.get('status'))

        result = self.controller.create_ride(self.ride_data)
        self.assertTrue(result.get('status'))

        resp = self.controller.make_response(
            {"Passenger": "m@y.com",
             "Ride Owner": "james",
             "Ride Name": "mwisho wa reli"})

        self.assertEqual(resp.get('message'), 'Request succesful')

    def retrieve_requests(self):
        """Test existing ride's requests can be retrieved."""
        res = self.controller.create_user(self.user_data)
        self.assertTrue(res.get('status'))

        result = self.controller.create_ride(self.ride_data)
        self.assertTrue(result.get('status'))

        self.controller.make_response(
            {"Passenger": "m@y.com",
             "Ride Owner": "james",
             "Ride Name": "mwisho wa reli"})
        init_len = len(self.controller.get_requests('mwisho wa reli', 'james'))
        self.controller.make_response(
            {"Passenger": "koigi@g.com",
             "Ride Owner": "james",
             "Ride Name": "mwisho wa reli"})

        new_len = len(self.controller.get_requests('mwisho wa reli', 'james'))
        self.assertEqual(new_len, init_len+1)
