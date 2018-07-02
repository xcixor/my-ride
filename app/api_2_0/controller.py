"""Interface views to the models."""
import psycopg2

from app.api_2_0.models import User


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
        return{'Status': True, 'Message': res.get('Message')}

    def drop_all(self):
        """Delete all tables."""
        connection = self.create_db_connection()
        res = self.user.delete_user_table(connection)
        if res.get('Status'):
            return{'Status': True, 'Message': res.get('Message')}
        return{'Status': True, 'Message': res.get('Message')}

    def create_user(self, user_data):
        """Create a user record."""
        connection = self.create_db_connection()
        email = user_data.get('Email')
        password = user_data.get('Password')
        confirm_password = user_data.get('Confirm Password')
        user_type = user_data.get('Type')
        res = self.user.create_user(connection, email, password,
                                   confirm_password, user_type)
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
