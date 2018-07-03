"""Interface views to the models."""
import psycopg2

from app.api_2_0.models import User
# from models import User


class Controller(object):
    """Perform db operations."""

    dbname = "rides"
    user = "rider"
    password = "pass123"
    host = "localhost"
    port = "5432"

    def __init__(self):
        """Initialize the controller.

        Args:
            db(dict): database connection information
        """
        self.user = User()

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
        if res.get("Status"):
            return{'Status': True, 'Message': res.get('Message')}
        return{'Status': False, 'Message': res.get('Message')}

    def drop_all(self):
        """Delete all tables."""
        connection = self.create_db_connection()
        res = self.user.delete_user_table(connection)
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
