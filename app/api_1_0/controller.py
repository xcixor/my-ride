"""Facilitates communication between the views and the models."""
from app.api_1_0.models import AppUser, Ride


class Controller(object):
    """Manipulates the model functionality."""

    def __init__(self):
        """Initialize objects."""
        self.user = AppUser()
        self.ride = Ride()

    def create_user(self, user_details):
        """Create a user for the application."""
        try:
            email = user_details.get('Email')
            user_type = user_details.get('Type')
            password = user_details.get('Password')
            confirm_password = user_details.get('Confirm Password')
        except KeyError as e:
            raise Exception("{} is required but is missing".format((e))) from e
        else:
            user_id = Controller.generate_id(self.user.app_users)
            user_data = {'Email': email, 'Password': password,
                         "Type": user_type, 'Confirm Password': confirm_password, 'Id': user_id}
            result = self.user.create_user(user_data)
            if result.get('Status'):
                return {'Status': True, 'Message': result.get('Message')}
            else:
                return {'Status': False, 'Message': result.get('Message')}

    @staticmethod
    def generate_id(item_data, item_id=0):
        """Create an id from the list of items provided.

        Args:
            items(iterable object)obejct from which id is determined.
            item_id(int): Initial id
        """
        if item_id == 0:
            item_id = len(item_data) + 1
        for key, value in item_data.items():
            if value['Id'] == int(item_id):
                item_id += 1
                Controller.generate_id(item_data, item_id)
        return item_id

    def login(self, logins):
        """Login in user with correct credentials."""
        email = logins.get('Email')
        password = logins.get('Password')
        res = self.user.login(email, password)
        if res.get('Status'):
            return {'Status': True, 'Message': res.get('Message')}
        else:
            return {'Status': False, 'Message': res.get('Message')}

    def create_ride(self, ride_details):
        """Create ride for logged in user."""
        owner = ride_details.get('Owner')
        date = ride_details.get('Date')
        time = ride_details.get('Time')
        name = '{}-{}-{}'.format(owner, date, time)
        ride_id = Controller.generate_id(self.ride.rides)
        ride_details.update({'Name': name, 'Id': ride_id, 'Requests': []})
        result = self.user.get_user(owner)
        if result.get('Status'):
            response = self.ride.create_ride(ride_details)
            if response.get('Status'):
                return {'Status': True, 'Message': response.get('Message')}
            else:
                return {'Status': False, 'Message': response.get('Message')}
        else:
            return {'Status': False, 'Message': 'That user does not exist'}

    def get_rides(self):
        """Get all rides from the rides model."""
        res = self.ride.get_rides()
        if res.get('Status'):
            return {'Status': True, 'Message': res.get('Message')}
        else:
            return {'Status': False, 'Message': res.get('Message')}

    def get_ride(self, owner, ride_id):
        """Fetch a ride."""
        result = self.user.get_user(owner)
        if result.get('Status'):
            res = self.ride.get_ride(owner, ride_id)
            if res.get('Status'):
                return {'Status': True, 'Message': res.get('Message')}
            else:
                return {'Status': False, 'Message': res.get('Message')}
        else:
            return {'Status': False, 'Message': 'User not registered'}

    def make_request(self, ride_id, owner, request_data):
        """Make a request for a ride."""
        res = self.ride.make_request(ride_id, owner, request_data)
        if res.get('Status'):
            return {'Status': True, 'Message': res.get('Message')}
        else:
            return {'Status': False, 'Message': res.get('Message')}

    def edit_ride(self, ride_id, owner, new_details):
        """Edit ride for registered user."""
        res = self.user.get_user(owner)
        if res.get('Status'):
            response = self.ride.edit_ride(ride_id, owner, new_details)
            if response.get('Status'):
                return {'Status': True, 'Message': response.get('Message')}
            else:
                return {'Status': False, 'Message': response.get('Message')}
        else:
            return {'Status': False, 'Message': 'User not registered'}
