"""Interface views to the models."""
from datetime import datetime
import psycopg2

from app.api_2_0.models import User, Ride, Request


class Controller(object):
    """Perform db operations."""

    dbname = ""
    user = ""
    password = ""
    host = ""
    port = ""

    def __init__(self):
        """Initialize the controller.

        Args:
            db(dict): database connection information
        """
        pass

    @classmethod
    def init_db(cls, db):
        """Get db configurations."""
        Controller.dbname = db.get('dbname')
        Controller.user = db.get('user')
        Controller.password = db.get('password')
        Controller.host = db.get('host')
        Controller.port = db.get('port')

    def create_all(self):
        """Create the db with all the tables.

        Args:
            db(dict): database connection information
        """
        user = User()
        ride = Ride()
        request = Request()
        connection = self.create_db_connection()
        res = user.create_user_table(connection)
        resp = ride.create_rides_table(connection)
        result = request.create_requests_table(connection)
        if res.get("Status") and resp.get('Status') and result.get('Status'):
            return{'Status': True, 'Message': 'All tables created'}
        return{'Status': False, 'Message':
                                {'User table error': res.get('Message'),
                                 'Rides table error': resp.get('Message')},
                                 'Request table error': result.get('Message')}

    def drop_all(self):
        """Delete all tables."""
        user = User()
        ride = Ride()
        request = Request()
        connection = self.create_db_connection()
        resp = request.delete_requests_table(connection)
        result = ride.delete_rides_table(connection)
        res = user.delete_user_table(connection)
        if res.get('Status'):
            return{'Status': True, 'Message': res.get('Message')}
        return{'Status': False, 'Message': res.get('Message')}

    def create_user(self, user_data):
        """Create a user record."""
        connection = self.create_db_connection()
        email = user_data.get('Email')
        password = user_data.get('Password')
        confirm_password = user_data.get('Confirm Password')
        user_type = user_data.get('Type')
        if self.is_empty(email):
            return {'Status': False, 'Message': 'Email cannot be blank'}
        user_details = {
            "email": email,
            "password": password,
            "confirm_password": confirm_password,
            "user_type": user_type
        }
        user = User(user_details)
        res = user.create_user(connection)
        if res.get('Status'):
            return {'Status': True, 'Message': res.get('Message')}
        return {'Status': False, 'Message': res.get('Message')}

    @classmethod
    def create_db_connection(cls):
        """Connect to the db."""
        connection = None
        try:
            db_url = "dbname={} user={} password={} host={} port={}".\
                      format(Controller.dbname, Controller.user, Controller.password,
                             Controller.host, Controller.port)
            connection = psycopg2.connect(db_url)
        except Exception as e:
            raise e
        return connection

    def verify_user_credentials(self, logins):
        """Verify user credentials to login."""
        user = User()
        email = logins.get('Email')
        password = logins.get('Password')
        connection = self.create_db_connection()
        res = user.find_user(connection, email)
        if res.get('Status'):
            if password == res.get('Message')[0][2]:
                return {'Status': True, "Message": 'Valid Credentials'}
            return {'Status': True, "Message": 'Valid Credentials'}
        return {'Status': False, 'Message': res.get('Message')}

    def is_empty(self, field):
        """Check that a value submitted is not whitespace characters."""
        if not field or not field.strip() or field.isspace():
            return True
        return False

    def is_valid_date(self, date_str):
        """Validate date format."""
        is_valid_date = True
        try:
            datetime.strptime(date_str, "%d/%m/%Y")
        except:
            is_valid_date = False
        return is_valid_date

    def validate_date(self, data_str):
        """Validate date not past."""
        if self.is_valid_date(data_str):
            date_to_validate = datetime.strptime(data_str, "%d/%m/%Y")
            now = datetime.now()
            if date_to_validate.date() > now.date():
                return {"Status": True}
            return {"Status": False, "Message": "{} is in the past".
                    format(data_str)}
        return {"Status": False,
                "Message": "Incorrect date format, should be DD/MM/YYYY"}

    def create_ride(self, ride_data):
        """Request models to create ride."""
        user = User()
        connection = self.create_db_connection()
        for key, value in ride_data.items():
            if type(value) == str:
                if self.is_empty(value):
                    return {'Status': False,
                            'Message': '{} is empty'.format(key)}
        owner = ride_data.get('Owner')
        owner_data = user.find_user(connection, owner).get('Message')
        owner_id = owner_data[0][0]
        date = ride_data.get('Date')
        time = ride_data.get('Time')
        identifier = '{}-{}-{}'.format(owner, date, time)
        ride_data.update({'Owner Id': owner_id})
        ride_data.update({'Identifier': identifier})

        resp = self.validate_date(date)
        ride = Ride(ride_data)
        if resp.get('Status'):
            res = ride.create_ride(connection)
            if res.get('Status'):
                return {'Status': True, 'Message': res.get('Message')}
            return {'Status': False, 'Message': res.get('Message')}
        return {"Status": False, "Message": resp.get('Message')}

    def get_rides(self):
        """Fetch rides from the model."""
        connection = self.create_db_connection()
        ride = Ride()
        res = ride.get_rides(connection)
        if res.get('Status'):
            return {'Status': True, 'Message': res.get('Message')}
        return {'Status': False, 'Message': res.get('Message')}

    def get_ride_by_id(self, ride_id):
        """Fetch a ride from db."""
        connection = self.create_db_connection()
        ride = Ride()
        res = ride.get_ride_by_id(connection, ride_id)
        if res.get('Status'):
            return {'Status': True, 'Message': res.get('Message')}
        return {'Status': False, 'Message': res.get('Message')}

    def request_ride(self, user, ride_id):
        """Make a ride request."""
        ride = Ride()
        app_user = User()
        connection = self.create_db_connection()
        owner_data = app_user.find_user(connection, user).get('Message')
        owner_id = owner_data[0][0]
        ride_data = ride.get_ride_by_id(connection, ride_id).get('Message')
        ride_owner = ride_data[0][9]
        if owner_id == ride_owner:
            return {'Status': False,
                    "Message": "You cant request your own ride"}
        request_data = {
            "Passenger Id": owner_id,
            "Email": user,
            "Ride Id": ride_id
        }
        request = Request(request_data)
        res = request.create_request(connection)
        if res.get('Status'):
            return {'Status': True, 'Message': res.get('Message')}
        return {'Status': False, 'Message': res.get('Message')}

    def get_requests(self, ride_id, user):
        """Request rides requests from db."""
        ride = Ride()
        app_user = User()
        request = Request()
        connection = self.create_db_connection()
        owner_data = app_user.find_user(connection, user).get('Message')
        owner_id = owner_data[0][0]
        ride = ride.get_ride_by_id(connection, ride_id)
        if ride.get('Status'):
            ride_data = ride.get('Message')
            ride_owner = ride_data[0]['Owner Id']
            if owner_id == ride_owner:
                requests = request.get_ride_requests(connection, ride_id)
                if requests.get('Status'):
                    return {'Status': True, 'Message': requests.get('Message')}
                return {'Status': False, 'Message': requests.get('Message')}
            return {'Status': False, 'Message': 'You dont have access to that ride'}
        return {'Status': False, 'Message': ride.get('Message')}

    def set_request_status(self, request_data, request_id, ride_id):
        """Accept or reject ride."""
        app_ride = Ride()
        request = Request()
        status = request_data.get('Status')
        connection = self.create_db_connection()
        ride = app_ride.get_ride_by_id(connection, ride_id)
        if not ride.get('Status'):
            return {'Status': False, 'Message': ride.get('Message')}
        result = request.set_request_status(connection, status, ride_id, request_id)
        if result.get('Status'):
            return {'Status': True, 'Message': result.get('Message')}
        return {'Status': True, 'Message': result.get('Message')}
