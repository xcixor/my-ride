"""Contains the classes for modelling the application."""
import re

from datetime import datetime


def is_empty(field):
    """Check that a value submitted is not whitespace characters."""
    if not field or not field.strip() or field.isspace():
        return True
    return False


def is_valid_date(date_str):
    """Validate date format."""
    is_valid_date = True
    try:
        datetime.strptime(date_str, "%d/%m/%Y")
    except:
        is_valid_date = False
    return is_valid_date


def validate_date(data_str):
    """Validate date not past."""
    if is_valid_date(data_str):
        date_to_validate = datetime.strptime(data_str, "%d/%m/%Y")
        now = datetime.now()
        if date_to_validate.date() > now.date():
            return {"Status": True}
        return {"Status": False, "Message": "{} is in the past".
                format(data_str)}
    return {"Status": False, "Message": "Incorrect date format, should be DD/MM/YYYY"}


class AppUser(object):
    """Handles user functionality."""

    def __init__(self):
        """Initialize an instance of the User class.

        Args:
            users(dict): Contains user records.
        """
        self.app_users = {}

    def create_user(self, user_details):
        """Register a new user.

        Args:
            user_details(dict): User details
        """
        email = user_details.get('Email')
        password = user_details.get('Password')
        if is_empty(email):
            return {'Status': False,
                    'Message': 'No value provided please check your input!'}
        confirm_password = user_details.get('Confirm Password')
        if email in self.app_users:
            return {"Status": False, "Message": "That user already exists"}
        elif not AppUser.verify_password_length(password):
            return {"Status": False,
                    "Message": "Password should not be less than six characters!"}
        elif not AppUser.verify_email(email):
            return {"Status": False, "Message": "Invalid email address!"}
        elif not password == confirm_password:
            return {"Status": True, "Message": "Passwords do not match!"}
        else:
            user = {email: user_details}
            self.app_users.update(user)
            return {"Status": True, "Message":
                    "{} Your account has bee Successfuly created".format(email)}

    @staticmethod
    def verify_email(email):
        """Check if email adress is valid.

        Returns:
        True if email is valid.

        """
        if re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",
                    email):
            return True

    @staticmethod
    def verify_password_length(password):
        """Check password is valid.

        Returns:
        True if password is long enough.

        """
        if len(password) >= 6:
            return True

    def get_user(self, email):
        """Retrieve a user from the users records.

        Returns user(dict):
        """
        if email in self.app_users:
            return {'Status': True, 'Message': self.app_users.get(email)}
        else:
            return {'Status': False, 'Message': 'That user is not registered'}

    def login(self, email, password):
        """Check if credentials are correct to allow login."""
        if is_empty(email):
            return {'Status': False, 'Message': 'No value provided please check your input!'}
        res = self.get_user(email)
        if res.get('Status'):
            if password == res.get('Message').get('Password'):
                return {'Status': True, 'Message': 'Login Successful'}
            else:
                return {'Status': False, 'Message': 'Invalid password email combination'}
        else:
            return {'Status': False, 'Message': res.get('Message')}


class Ride(object):
    """Handles ride functionality."""

    def __init__(self):
        """Initialize an instance of the Ride class.

        Args:
            rides(dict): Contains user records.
        """
        self.rides = {}

    def create_ride(self, ride_data):
        """Create a new ride.

        Args:
            ride_data(dict): the ride's data
        """
        try:
            owner = ride_data.get('Owner')
            name = ride_data.get('Name')
        except KeyError as e:
            raise Exception("{} is required but is missing".format((e))) from e

        for key, value in ride_data.items():
            if type(value) == str:
                if is_empty(value):
                    return {'Status': False, 'Message': '{} is empty'.format(key)}

        date_str = ride_data.get('Date')
        res = validate_date(date_str)
        if res.get('Status'):
            if owner in self.rides:
                if name in self.rides.get(owner):
                    return {'Status': False,
                            'Message': 'That ride already exist'}
                else:
                    driver_rides = self.rides.get(owner)
                    driver_rides.update({name: ride_data})
                    return {'Status': True,
                            'Message': 'Your rides have been updated'}
            else:
                new_ride = {owner: {name: ride_data}}
                self.rides.update(new_ride)
                return {'Status': True,
                        'Message': '{} Your first ride has been created'.
                        format(owner)}
        return {"Status": False, "Message": res.get('Message')}

    def get_rides(self):
        """Return all rides created."""
        if not bool(self.rides):
            return {'Status': False,
                    'Message': 'There are no rides at this moment'}
        else:
            return {'Status': True, 'Message': self.rides}

    def get_ride_by_id(self, owner, ride_id):
        """Fetch ride by Id.

        Args:
            ride_id(int): Unique identifier of the ride
            owner(str): Name of user who created the ride
        """
        user_rides = self.rides.get(owner)
        if user_rides:
            for key, value in user_rides.items():
                if value.get('Id') == int(ride_id):
                    return {'Status': True, 'Message': value}
                else:
                    return {'Status': False,
                            'Message': 'Ride for that id is inexistent'}
        else:
            return {'Status': False, 'Message': 'No rides for this user'}

    def get_ride(self, owner, ride_id):
        """Fetch a single ride."""
        res = self.get_ride_by_id(owner, ride_id)
        if res.get('Status'):
            return {'Status': True, 'Message': res.get('Message')}
        else:
            return {'Status': False, 'Message': res.get('Message')}

    def make_request(self, ride_id, owner, request_data):
        """Make a request to join a ride.

        Args:
            ride_id(int): Unique identifier of the ride
            owner(str): Name of user who created the ride
            request_data(dict): request details
        """
        res = self.get_ride_by_id(owner, ride_id)
        if res.get('Status'):
            user_requests = res.get('Message').get('Requests')
            user_requests.append(request_data)
            return {'Status': True, 'Message': 'Request made successfuly'}
        else:
            return {'Status': False, 'Message': 'That ride does not exist'}

    def get_requests(self, owner, ride_id):
        """Get a ride's requests.

        Args:
            ride_id(int): Unique identifier of the ride
            owner(str): Name of user who created the ride
        """
        res = self.get_ride_by_id(owner, ride_id)
        if res.get('Status'):
            user_requests = res.get('Message').get('Requests')
            return {'Status': True, 'Message': user_requests}
        else:
            return {'Status': False, 'Message': 'That ride does not exist'}

    def edit_ride(self, ride_id, owner, new_details):
        """Edit the details of a ride.

        Args:
            ride_id(int): Unique identifier of the ride
            owner(str): Name of user who created the ride
            new_details(dict): New details of the ride
        """
        for key, value in new_details.items():
            if type(value) == str:
                if is_empty(value):
                    return {'Status': False, 'Message': '{} is empty'.
                            format(key)}
                result = self.get_ride_by_id(owner, ride_id)
                if result.get('Status'):
                    ride_to_edit = result.get('Message')
                    for key, value in new_details.items():
                        ride_to_edit[key] = value
                    return {'Status': True, 'Message': ride_to_edit}
                return {'Status': False, 'Message': result.get('Message')}
