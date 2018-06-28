import unittest

from app import create_app, DB

from app.api_2_0.models import User


class TestUserModel(unittest.TestCase):

    """Tests the user model."""
    def setUp(self):
        """Create app context and initialize db."""
        self.user = User()

    def tearDown(self):
        """Remove app context, remove db session and delete all records."""
        del self.user

    def test_email_verification_success(self):
        """Verfiy email address."""
        self.assertFalse(self.user.verify_email('pndungu.com'))

    def test_password_verification_success(self):
        """Test password length."""
        self.assertFalse(self.user.check_password_length('pass12'))

    def test_passwords_match_success(self):
        """Test passwords provided match."""
        self.assertTrue(self.user.confirm_password('pass123', 'pass123'))