import unittest

from app import create_app

from app.api_2_0.models import User


class TestUserModel(unittest.TestCase):

    """Tests the user model."""
    def setUp(self):
        """Create app object."""
        self.user = User()

    def tearDown(self):
        """Remove app object"""
        del self.user

    def test_email_verification_success(self):
        """Verfiy email address."""
        self.assertFalse(self.user.verify_email('pndungu.com'))

    def test_password_verification_success(self):
        """Test password length."""
        self.assertFalse(self.user.check_password_length('pass1'))

    def test_passwords_match_success(self):
        """Test passwords provided match."""
        self.assertTrue(self.user.confirm_password('pass123', 'pass123'))

    def test_invalid_date_false(self):
        """Test valid date is given."""
        self.assertFalse(self.user.validate_date('2000/2000/2000'))

    def test_past_date_false(self):
        """Test user cannot pass a date in the past."""
        self.assertFalse(self.validate_date('20/2/2018'))

    def test_empty_user_fields_false(self):
        """Test blank user fields not allowed."""
        self.assertFalse(self.validate_field("    "))