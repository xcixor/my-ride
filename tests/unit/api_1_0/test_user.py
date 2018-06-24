"""Contains tests for User class."""
import unittest
from app.api_1_0.models import User


class TestUser(unittest.TestCase):
    """Tests User class."""

    def setUp(self):
        """Initialize objects to use during testing."""
        self.user = User()
        self.user_data = {
            "Email": "wamai@gmail.com",
            "Password": "pass123",
            "Confirm Password": "pass123"
        }

    def tearDown(self):
        """Delete objects for next method."""
        del self.user
        del self.user_data

    def test_create_user_with_mandatory_fields_success(self):
        """Test user can be created successfuly."""
        res = self.user.create_user(self.user_data)
        self.assertTrue(res)

    def get_user_if_registered_success(self):
        """Test get user profile."""
        self.user.create_user(self.user_data)
        self.assertDictContainsSubset(self.user_data, self.user.get_user(1))

    def test_register_user_invalid_email_false(self):
        """Test user cannot register with invalid email."""
        user = {"Email": "dong.com", "Password": "pass123",
                "Confirm Password": "pass123"}
        res = self.user.create_user(user)
        self.assertEqual(res.get('message'), "Invalid email address")

    def test_register_user_short_password_false(self):
        """Test user cannot register with a verys short password."""
        user = {"Email": "dong@.com", "Password": "pass123",
                "Confirm Password": "pass123"}
        res = self.user.create_user(user)
        self.assertEqual(res.get('message'), 'Password should not be less \
                         than eight charcters')

    def test_create_user_if_already_registred_false(self):
        """Test the same user cannot create an account twice."""
        self.user.create_user(self.user_data)
        res = self.user.create_user(self.user_data)
        self.assertEqual(res.get('message'), 'That user already exists')

    def test_update_user_details_success(self):
        """Test user can update their user details."""
        self.user.create_user(self.user_data)
        details = {"Password": "pass123", "National Id": "29811039",
                   "Alternate Cell": "+2547238484", "Email": "m@g.com"}
        self.user.update_user('wamai@gmail.com', details)
        self.assertDictContainsSubset(details, self.user.get_user(1))

    def test_delete_user_if_exist_success(self):
        """Test delete user successfuly."""
        self.user.create_user(self.user_data)
        res = self.user.delete_user('wamai@.com')
        self.assertTrue(res)
