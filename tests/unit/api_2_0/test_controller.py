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
            "Email": "p@gmail.com",
            "Type": False,
            "Password": "pass123",
            "Confirm Password": "pass123"
        }
        self.ride = {
            "Ride Name": "V8",
            "Origin": "Thika",
            "Destination": "Nyeri",
            "Time": "8: 30",
            "Name": "voyage to meru",
            "Date": "12/8/2018",
            "No Plate": "KCE 323 B",
            "Owner Id": 1,
            "Capacity": "6"
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
        print('***************', resp.get('Message'))
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
        self.assertEqual(res.get('Message'), 'Email cannot be empty!')

    def test_create_ride_with_invalid_date_false(self):
        res = self.controller.create_user(self.driver)
        self.assertTrue(res.get('Status'))
        """Test controller can detect invalid date."""
        ride = {
            "Ride Name": "V8",
            "Origin": "Thika",
            "Destination": "Nyeri",
            "Time": "8: 30",
            "Name": "voyage to meru",
            "Owner Id": 1,
            "No Plate": "KCE 323 B",
            "Date": "102/78/2018",
            "Capacity": "6"
        }
        res = self.controller.create_ride(ride)
        self.assertEqual(res.get('Message'), 'Invalid date')

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
            "Owner Id": 1,
            "Date": "12/6/2017",
            "Capacity": "6"
        }
        res = self.controller.create_ride(ride)
        self.assertEqual(res.get('Message'), 'Date provided is in the past!')

    def test_create_ride_success(self):
        """Test ride can be created with accurate data."""
        res = self.controller.create_user(self.driver)
        self.assertTrue(res.get('Status'))
        res = self.controller.create_ride(self.ride)
        self.assertEqual(res.get('Message'),
                         'Your ride has been created successfuly')

    def test_driver_request_own_ride_false(self):
        """Test driver cannot request own ride."""
        res = self.controller.create_user(self.driver)
        self.assertTrue(res.get('Message'))
        resp = self.controller.request_ride({"User Id": 1})
        self.assertFalse(resp.get('Status'))

    def get_all_rides_if_exist_success(self):
        """Test existing rides can be displayed."""
        res = self.controller.create_user(self.driver)
        self.assertTrue(res.get('Status'))
        res = self.controller.create_ride(self.ride)
        self.assertEqual(res.get('Message'),
                         'Your ride has been created successfuly')
        resp = self.controller.get_all_rides()
        self.assertDictContainsSubset(resp.get('Message'), self.ride)

    def test_create_ride_for_non_exisiting_user_false(self):
        """Test a ride cannot be created if user not created."""
        res = self.controller.create_ride(self.ride)
        self.assertEqual(res.get('Message'),
                         'Your ride has been created successfuly')

    def test_get_ride_success(self):
        """Test existing ride can be displayed."""
        res = self.controller.create_user(self.driver)
        self.assertTrue(res.get('Status'))
        res = self.controller.create_ride(self.ride)
        self.assertEqual(res.get('Message'),
                         'Your ride has been created successfuly')
        resp = self.controller.get_ride_by_id(1)
        self.assertDictContainsSubset(resp.get('Message'), self.ride)

    def test_make_ride_request_success(self):
        """Test a ride can be requested successfuly."""
        res = self.controller.create_user(self.driver)
        self.assertTrue(res.get('Status'))
        res = self.controller.create_ride(self.ride)
        self.assertEqual(res.get('Message'),
                         'Your ride has been created successfuly')
        res = self.controller.create_user(self.passenger)
        self.assertTrue(res.get('Message'))
        resp = self.controller.request_ride({"User Id": 1})
        self.assertTrue(resp.get('Status'))

    def test_get_ride_requests_success(self):
        """Test requests for a ride can be displayed."""
        res = self.controller.create_user(self.driver)
        self.assertTrue(res.get('Status'))
        res = self.controller.create_ride(self.ride)
        self.assertEqual(res.get('Message'),
                         'Your ride has been created successfuly')
        res = self.controller.create_user(self.passenger)
        self.assertTrue(res.get('Message'))
        resp = self.controller.request_ride({"User Id": 1})
        self.assertTrue(resp.get('Status'))
        result = self.controller.get_ride_requests(1)
        self.assertDictContainsSubset(result.get('Message'), self.ride)

    def test_user_reject_ride_success(self):
        """Test user can reject a request successfuly."""
        res = self.controller.create_user(self.driver)
        self.assertTrue(res.get('Status'))
        res = self.controller.create_ride(self.ride)
        self.assertEqual(res.get('Message'),
                         'Your ride has been created successfuly')
        res = self.controller.create_user(self.passenger)
        self.assertTrue(res.get('Message'))
        resp = self.controller.request_ride({"User Id": 1})
        self.assertTrue(resp.get('Status'))
        res = self.controller.reject_request(1, {"Request Id": 1})
        self.assertTrue(res.get('Status'))

    def test_user_can_accept_ride_success(self):
        """Test user can accept a ride successfuly."""
        res = self.controller.create_user(self.driver)
        self.assertTrue(res.get('Status'))
        res = self.controller.create_ride(self.ride)
        self.assertEqual(res.get('Message'),
                         'Your ride has been created successfuly')
        res = self.controller.create_user(self.passenger)
        self.assertTrue(res.get('Message'))
        resp = self.controller.request_ride(1, {"User Id": 1})
        self.assertTrue(resp.get('Status'))
        res = self.controller.accept_request(1, {"Request Id": 1})
        self.assertTrue(res.get('Status'))

    def test_get_user_profile_success(self):
        """Test user can get their user profile."""
        res = self.controller.create_user(self.driver)
        self.assertTrue(res.get('Status'))
        resp = self.controller.get_user_profile(1)
        self.assertDictContainsSubset(resp.get('Message'), \
                                      {"Email": "p@g.com"})

    def test_edit_profile_success(self):
        """Test user can edit their profile successfuly."""
        res = self.controller.create_user(self.driver)
        self.assertTrue(res.get('Status'))
        new_details = {
            "Email": "peter@gmail.com"
            }
        result = self.controller.edit_profile('pass123', new_details)
        self.assertTrue(result.get('Status'))

    def test_edit_ride_success(self):
        """Test existing ride can be edited successfuly."""
        res = self.controller.create_user(self.driver)
        self.assertTrue(res.get('Status'))
        res = self.controller.create_ride(self.ride)
        self.assertEqual(res.get('Message'),
                         'Your ride has been created successfuly')
        new_data = {
            "Ride Name": "Mathree",
            "Origin": "Nyahururu",
            "Destination": "Ngwaroz"
        }
        resp = self.controller.edit_ride(new_data)
        self.assertDictContainsSubset(self.controller.get_ride_by_id(1),\
                                      new_data)

    def test_delete_ride_success(self):
        """Test existing ride can be deleted."""
        res = self.controller.create_user(self.driver)
        self.assertTrue(res.get('Status'))
        res = self.controller.create_ride(self.ride)
        result = self.controller.delete_ride(1)
        self.assertTrue(result)

    def test_invalid_date_false(self):
        """Test valid date is given."""
        self.assertFalse(self.controller.validate_date('2000/2000/2000'))

    def test_past_date_false(self):
        """Test ride cannot pass a date in the past."""
        self.assertFalse(self.controller.validate_date('20/2/2018'))

    def test_empty_ride_fields_false(self):
        """Test blank ride fields not allowed."""
        self.assertFalse(self.controller.validate_field("    "))
