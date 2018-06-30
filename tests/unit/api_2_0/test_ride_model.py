import unittest

from app.api_2_0.models import Ride


class TestRideModel(unittest.TestCase):

    """Tests the ride model."""

    def setUp(self):
        """Create app context and initialize db."""
        self.ride = Ride()

    def tearDown(self):
        """Remove app context, remove db session and delete all records."""
        del self.ride

    def test_invalid_date_false(self):
        """Test valid date is given."""
        self.assertFalse(self.ride.validate_date('2000/2000/2000'))

    def test_past_date_false(self):
        """Test ride cannot pass a date in the past."""
        self.assertFalse(self.validate_date('20/2/2018'))

    def test_empty_ride_fields_false(self):
        """Test blank ride fields not allowed."""
        self.assertFalse(self.validate_field("    "))
