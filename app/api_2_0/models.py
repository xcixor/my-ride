"""Contains logic to create and manipulate users."""
import re
import psycopg2
from flask_bcrypt import Bcrypt

BCRYPT = Bcrypt()


def is_empty(field):
    """Check that a value submitted is not whitespace characters."""
    if not field or not field.strip() or field.isspace():
        return True
    return False


class User(object):
    """Handles user transactions."""

    def __init__(self):
        """Create the user table."""
        pass

    def create_user_table(self, connection):
        """Create user table."""
        conn = connection
        cursor = conn.cursor()
        try:
            query = "CREATE TABLE users (id serial PRIMARY KEY, \
                                         Email VARCHAR, \
                                         User_Password VARCHAR, \
                                         Driver Boolean);"
            cursor.execute(query)
            conn.commit()
            conn.close()
            return {'Status': True, 'Message': 'Success!'}
        except Exception as e:
            return {'Status': False, 'Message': e}

    def delete_user_table(self, connection):
        """Delete the user table."""
        conn = connection
        cursor = conn.cursor()
        try:
            query = "DROP TABLE users;"
            cursor.execute(query)
            conn.commit()
            conn.close()
            return {'Status': True, 'Message': 'Success!'}
        except Exception as e:
            return {'Status': False, 'Message': e}

    def create_db_connection(self):
        """Connect to the db."""
        connection = None
        try:
            connection = psycopg2.connect("dbname='rides' user='rider' \
            password='pass123' host='localhost' port='5432'")
        except Exception as e:
            raise e
        return connection

    def create_user(self, connection, email, password, confirm_password, user_type):
        """Create user record."""
        if self.find_user(email).get('Status'):
            return {'Status': False, 'Message': 'User already exists'}
        conn = connection
        cursor = conn.cursor()
        try:
            if not is_empty(email):
                if User.verify_email(email):
                    if User.check_password_length(password):
                        if User.confirm_password(password, confirm_password):
                            user_pass = BCRYPT.generate_password_hash(password)
                            query = "insert into users (email, user_password, driver) values ('{}', '{}', '{}');".format(email, password, user_type)
                            cursor.execute(query)
                            conn.commit()
                            conn.close()
                            return {"Status": True, "Message": "Succesfuly created user record"}
                        return {"Status": False, "Message": "Passwords dont match!"}
                    return {"Status": False, "Message": "Password should not be less than six characters"}
                return {"Status": False, "Message": "Invalid email Address!"}
            return {"Status": False, "Message": "Email cannot be blank!"}
        except Exception as e:
            return {"Status": False, "Message": e}

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
        cursor.execute("SELECT * FROM users WHERE Email='{}';".format(email))
        rows = cursor.fetchall()
        if rows:
            return {'Status': True, 'Message': rows}
        return {'Status': False, 'Message': 'User not found'}
