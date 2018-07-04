"""Test the controller."""
from app import create_app
import unittest

from app.api_2_0.controller import Controller


class TestController(unittest.TestCase):
    """Contains test for Controller functioanlity."""

    def setUp(self):
        """Init object for use in tests."""
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.controller = Controller()

        self.driver = {
            "Email": "p@gmail.com",
            "Type": True,
            "Password": "pass123",
            "Confirm Password": "pass123"
        }
        self.passenger = {
            "Email": "pr@gmail.com",
            "Type": False,
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
        """Remove object after test."""
        self.controller.drop_all()
        del self.controller
        self.app_context.pop()

    def test_create_db_connection_success(self):
        """Test controller prepares app with db on app creation."""
        self.assertIsNotNone(self.controller.create_db_connection())

    def test_create_user_success(self):
        """Test controller can handle user creation."""
        res = self.controller.create_user(self.driver)
        self.assertTrue(res.get('Status'))

    def test_delete_all_tables_success(self):
        """Test can handle the deletion of all app tables."""
        res = self.controller.drop_all()
        self.assertTrue(res.get('Status'))
        resp = self.controller.create_user(self.driver)
        self.assertFalse(resp.get('Status'))
        self.assertIn('current transaction is aborted', resp.get('Message'))

    def test_create_all_tables_success(self):
        """Test controller creates all databases."""
        resp = self.controller.create_all()
        self.assertTrue(resp.get('Status'))

    def test_verify_user_logins_success(self):
        """Test controller can check if user can login."""
        res = self.controller.create_user(self.driver)
        self.assertTrue(res.get('Status'))
        logins = {
            "Email": "p@gmail.com",
            "Password": "pass123"
        }
        res = self.controller.verify_user_credentials(logins)
        self.assertEqual(res.get('Message'), 'Valid Credentials')

    def test_make_request_with_empty_fields_false(self):
        """Test controller can handle data validation."""
        user = {
            "Email": "    ",
            "Type": True,
            "Password": "pass123",
            "Confirm Password": "pass123"
        }
        res = self.controller.create_user(user)
        self.assertEqual(res.get('Message'), 'Email cannot be blank')

    def test_create_ride_with_invalid_date_false(self):
        """Test cannot create ride with invalid date."""
        res = self.controller.create_user(self.driver)
        self.assertTrue(res.get('Status'))
        ride = {
            "Ride Name": "V8",
            "Origin": "Thika",
            "Destination": "Nyeri",
            "Time": "8: 30",
            "Name": "voyage to meru",
            "Owner": "p@gmail.com",
            "No Plate": "KCE 323 B",
            "Date": "102-78/2018",
            "Capacity": "6"
        }
        resp = self.controller.create_ride(ride)
        self.assertEqual(resp.get('Message'),
                         'Incorrect date format, should be DD/MM/YYYY')

    def test_create_ride_with_past_date_false(self):
        res = self.controller.create_user(self.driver)
        self.assertTrue(res.get('Status'))
        """Test controller can detect invalid date."""
        ride = {
            "Ride Name": "V8",
            "Origin": "Thika",
            "Destination": "Nyeri",
            "Time": "8: 30",
            "Name": "voyage to meru",
            "No Plate": "KCE 323 B",
            "Owner": "p@gmail.com",
            "Date": "12/6/2017",
            "Capacity": "6"
        }
        res = self.controller.create_ride(ride)
        self.assertEqual(res.get('Message'),
                         '12/6/2017 is in the past')

    def test_create_ride_success(self):
        """Test ride can be created with accurate data."""
        res = self.controller.create_user(self.driver)
        self.assertTrue(res.get('Status'))
        res = self.controller.create_ride(self.ride)
        self.assertEqual(res.get('Message'),
                         'Succesfuly created ride!')

    def test_driver_request_own_ride_false(self):
        """Test driver cannot request own ride."""
        res = self.controller.create_user(self.driver)
        self.assertTrue(res.get('Message'))
        res = self.controller.create_ride(self.ride)
        self.assertEqual(res.get('Message'),
                         'Succesfuly created ride!')
        resp = self.controller.request_ride('p@gmail.com', 1)
        self.assertFalse(resp.get('Status'))

    def get_all_rides_if_exist_success(self):
        """Test existing rides can be displayed."""
        res = self.controller.create_user(self.driver)
        self.assertTrue(res.get('Status'))
        res = self.controller.create_ride(self.ride)
        self.assertEqual(res.get('Message'),
                         'Succesfuly created ride!')
        resp = self.controller.get_rides()
        print(resp)
        self.assertDictContainsSubset(resp.get('Message'), self.ride)

    def test_create_ride_for_non_exisiting_user_false(self):
        """Test a ride cannot be created if user not created."""
        res = self.controller.create_ride(self.ride)
        self.assertFalse(res.get('Status'))

    def test_create_ride_with_empty_fields_false(self):
        """Test cannot create ride with invalid date."""
        res = self.controller.create_user(self.driver)
        self.assertTrue(res.get('Status'))
        ride = {
            "Ride Name": "",
            "Origin": "Thika",
            "Destination": "Nyeri",
            "Time": "8: 30",
            "Name": "voyage to meru",
            "Owner": "p@gmail.com",
            "No Plate": "KCE 323 B",
            "Date": "102-78/2018",
            "Capacity": "6"
        }
        resp = self.controller.create_ride(ride)
        self.assertEqual(resp.get('Message'),
                         'Ride Name is empty')

    def test_get_ride_success(self):
        """Test existing ride can be displayed."""
        res = self.controller.create_user(self.driver)
        self.assertTrue(res.get('Status'))
        res = self.controller.create_ride(self.ride)
        self.assertEqual(res.get('Message'),
                         'Succesfuly created ride!')
        self.assertTrue(self.controller.get_rides().get('Message'))

    def test_make_ride_request_success(self):
        """Test a ride can be requested successfuly."""
        res = self.controller.create_user(self.driver)
        self.assertTrue(res.get('Status'))
        res = self.controller.create_ride(self.ride)
        self.assertEqual(res.get('Message'),
                         'Succesfuly created ride!')
        res = self.controller.create_user(self.passenger)
        self.assertTrue(res.get('Message'))
        resp = self.controller.request_ride('pr@gmail.com', 1)
        self.assertEqual(resp.get('Message'), 'Succesfuly made request!')

    def test_get_ride_requests_success(self):
        """Test requests for a ride can be displayed."""
        res = self.controller.create_user(self.driver)
        self.assertTrue(res.get('Status'))
        res = self.controller.create_ride(self.ride)
        self.assertEqual(res.get('Message'),
                         'Succesfuly created ride!')
        res = self.controller.create_user(self.passenger)
        self.assertTrue(res.get('Message'))

        resp = self.controller.request_ride('pr@gmail.com', 1)
        self.assertEqual(resp.get('Message'), 'Succesfuly made request!')

        requests = self.controller.get_requests(1, 'p@gmail.com')
        self.assertEqual(len(requests.get('Message')), 1)

    def test_user_reject_ride_success(self):
        """Test user can reject a request successfuly."""
        res = self.controller.create_user(self.driver)
        self.assertTrue(res.get('Status'))
        res = self.controller.create_ride(self.ride)
        self.assertEqual(res.get('Message'),
                         'Succesfuly created ride!')
        res = self.controller.create_user(self.passenger)
        self.assertTrue(res.get('Message'))

        resp = self.controller.request_ride('pr@gmail.com', 1)
        self.assertEqual(resp.get('Message'), 'Succesfuly made request!')

        request_data = {'Status': False}

        result = self.controller.set_request_status(request_data, 1, 1)
        self.assertEqual('request updates succesfuly', result.get('Message'))

    def test_user_can_accept_ride_success(self):
        """Test user can accept a ride successfuly."""
        res = self.controller.create_user(self.driver)
        self.assertTrue(res.get('Status'))
        res = self.controller.create_ride(self.ride)
        self.assertEqual(res.get('Message'),
                         'Succesfuly created ride!')
        res = self.controller.create_user(self.passenger)
        self.assertTrue(res.get('Message'))

        resp = self.controller.request_ride('pr@gmail.com', 1)
        self.assertEqual(resp.get('Message'), 'Succesfuly made request!')

        request_data = {'Status': True}

        result = self.controller.set_request_status(request_data, 1, 1)
        self.assertEqual('request updates succesfuly', result.get('Message'))
