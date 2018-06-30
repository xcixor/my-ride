"""Interface views to the models."""
import psycopg2

from models import User

class Controller(object):
    """Perform db operations."""

    def __init__(self):
        self.user = User()

    def create_all(self, dbname, user, password, host, port):
        """Create the db with all the tables."""
        connection = self.create_db_connection(dbname, user, password, host, port)
        res = self.user.create_user_table(connection)
        if res.get("Status"):
            print(res.get('Message'))
        print(res.get('Message'))

    def drop_all(self, dbname, user, password, host, port):
        """Delete all tables."""
        connection = self.create_db_connection(
            dbname, user, password, host, port)
        res = self.user.delete_user_table(connection)
        if res.get('Status'):
            print(res.get('Message'))
        print(res.get('Message'))

    def create_user(self, dbname, user, password, host, port, email, user_password, confirm_password, user_type):
        """Create a user record."""
        connection = self.create_db_connection(
            dbname, user, password, host, port)
        res = self.user.create_user(connection, email, password, confirm_password, user_type)
        if res.get('Status'):
            print(res.get('Message'))
        print(res.get('Message'))


    def create_db_connection(self, dbname, user, password, host, port):
        """Connect to the db."""
        connection = None
        try:
            db_url = "dbname={} user={} password={} host={} port={}".format(dbname, user, password, host, port)
            connection = psycopg2.connect(db_url)
        except Exception as e:
            raise e
        return connection
