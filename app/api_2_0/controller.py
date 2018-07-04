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
        self.user = User()
        self.ride = Ride()
        self.request = Request()

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
        connection = self.create_db_connection()
        res = self.user.create_user_table(connection)
        resp = self.ride.create_rides_table(connection)
        result = self.request.create_requests_table(connection)
        if res.get("Status") and resp.get('Status') and result.get('Status'):
            return{'Status': True, 'Message': 'All tables created'}
        return{'Status': False, 'Message':
                                {'User table error': res.get('Message'),
                                 'Rides table error': resp.get('Message')},
                                 'Request table error': result.get('Message')}

    def drop_all(self):
        """Delete all tables."""
        connection = self.create_db_connection()
        resp = self.request.delete_requests_table(connection)
        result = self.ride.delete_rides_table(connection)
        res = self.user.delete_user_table(connection)
        print('ERro from cont', res.get('Message'))
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
        res = self.user.create_user(connection, user_details)
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
        email = logins.get('Email')
        password = logins.get('Password')
        connection = self.create_db_connection()
        res = self.user.find_user(connection, email)
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
        connection = self.create_db_connection()
        for key, value in ride_data.items():
            if type(value) == str:
                if self.is_empty(value):
                    return {'Status': False,
                            'Message': '{} is empty'.format(key)}
        owner = ride_data.get('Owner')
        owner_data = self.user.find_user(connection, owner).get('Message')
        owner_id = owner_data[0][0]
        date = ride_data.get('Date')
        time = ride_data.get('Time')
        identifier = '{}-{}-{}'.format(owner, date, time)
        ride_data.update({'Owner Id': owner_id})
        ride_data.update({'Identifier': identifier})

        resp = self.validate_date(date)
        if resp.get('Status'):
            res = self.ride.create_ride(connection, ride_data)
            if res.get('Status'):
                return {'Status': True, 'Message': res.get('Message')}
            return {'Status': False, 'Message': res.get('Message')}
        return {"Status": False, "Message": resp.get('Message')}

    def get_rides(self):
        """Fetch rides from the model."""
        connection = self.create_db_connection()
        res = self.ride.get_rides(connection)
        if res.get('Status'):
            return {'Status': True, 'Message': res.get('Message')}
        return {'Status': False, 'Message': res.get('Message')}

    def get_ride_by_id(self, ride_id):
        """Fetch a ride from db."""
        connection = self.create_db_connection()
        res = self.ride.get_ride_by_id(connection, ride_id)
        if res.get('Status'):
            return {'Status': True, 'Message': res.get('Message')}
        return {'Status': False, 'Message': res.get('Message')}

    def request_ride(self, user, ride_id):
        """Make a ride request."""
        connection = self.create_db_connection()
        owner_data = self.user.find_user(connection, user).get('Message')
        owner_id = owner_data[0][0]
        ride_data = self.ride.get_ride_by_id(connection, ride_id).get('Message')
        ride_owner = ride_data[0][9]
        if owner_id == ride_owner:
            return {'Status': False,
                    "Message": "You cant request your own ride"}
        res = self.request.create_request(connection, {
            "Passenger Id": owner_id,
            "Ride Id": ride_id,
            'Email': user
        })
        if res.get('Status'):
            return {'Status': True, 'Message': res.get('Message')}
        return {'Status': False, 'Message': res.get('Message')}

    def get_requests(self, ride_id, user):
        """Request rides requests from db."""
        connection = self.create_db_connection()
        owner_data = self.user.find_user(connection, user).get('Message')
        owner_id = owner_data[0][0]
        ride = self.ride.get_ride_by_id(connection, ride_id)
        ride_data = ride.get('Message')
        ride_owner = ride_data[0][9]
        if ride.get('Status'):
            if owner_id == ride_owner:
                requests = self.request.get_ride_requests(connection, ride_id)
                if requests.get('Status'):
                    return {'Status': True, 'Message': requests.get('Message')}
                return {'Status': False, 'Message': requests.get('Message')}
            return {'Status': False, 'Message': 'You dont have access to that ride'}
        return {'Status': False, 'Message': ride.get('Message')}
