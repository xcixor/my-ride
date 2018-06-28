"""Contains logic to create and manipulate users."""
import re
import psycopg2
from flask_bcrypt import Bcrypt

BCRYPT = Bcrypt()

class User(object):
    """Handles user transactions."""

    def __init__(self):
        """Create the user table."""
        conn = psycopg2.connect("dbname='rides' user='rider' password='pass123' \
                                 host='localhost' port='5432'")
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS user \
                      (Email varchar(40) NOT NULL, Password varchar(256) NOT NULL, \
                      Usertype varchar(40) NOT NULL)")
        conn.commit()
        conn.close()

    def create_db_connection(self):
        """Connect to the db."""
        connection = None
        try:
            connection = psycopg2.connect("dbname='rides' user='rider' \
            password='pass123' host='localhost' port='5432'")
        except Exception as e:
            raise e
        return connection

    def create_user(self, email, password, confirm_password, user_type):
        """Create user record."""
        if self.find_user(email).get('Status'):
            return {'Status': False, 'Message': 'User already exists'}
        connection = self.create_db_connection()
        cursor = connection.cursor()
        try:
            if User.verify_email(email) and \
                User.check_password_length(password) and \
                User.confirm_password(password, confirm_password):
                user_pass = BCRYPT.generate_password_hash(password)
                cursor.execute('INSERT INTO user VALUES(?, ?, ?)', (email, user_pass, user_type))
                connection.commit()
                connection.close()
                return {'Status': True, 'Message': 'User created!'}
        except Exception as e:
            return {'Message': e, "Status": False}

    @staticmethod
    def verify_email(email):
        """Verify email address."""
        if re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",
                    email):
            return True

    @staticmethod
    def check_password_length(password):
        """Check password length."""
        if len(password) >= 6:
            return True

    @staticmethod
    def confirm_password(password, confirm_password):
        """Confirm passwords match."""
        if password == confirm_password:
            return True

    def find_user(self, email):
        """Retrieve user from db."""
        connection = self.create_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM store WHERE Email=?", (email))
        rows = cursor.fetchall()
        if rows:
            return {'Status': True, 'Message': rows}
