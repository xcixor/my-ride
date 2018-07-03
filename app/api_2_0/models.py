"""Contains logic to create and manipulate users."""
import re
import psycopg2
from flask_bcrypt import Bcrypt

BCRYPT = Bcrypt()


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
                                         User_Password TEXT, \
                                         FirstName TEXT,\
                                         LastName TEXT, \
                                         Gender TEXT,\
                                         Joined TEXT, \
                                         Tel TEXT, \
                                         Ridename TEXT, \
                                         Ride_Registration TEXT, \
                                         Driver Boolean);"
            cursor.execute(query)
            conn.commit()
            conn.close()
            return {'Status': True, 'Message': 'Success!'}
        except Exception as e:
            return {'Status': False, 'Message': '{}'.format(e)}

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

    def create_user(self, connection, user_data):
        """Create user record."""
        email = user_data.get('email')
        password = user_data.get('password')
        confirm_password = user_data.get('confirm_password')
        user_type = user_data.get('user_type')

        if self.find_user(connection, email).get('Status'):
            return {'Status': False, 'Message': 'User already exists'}
        conn = connection
        cursor = conn.cursor()
        try:
            if User.verify_email(email):
                if User.check_password_length(password):
                    if User.confirm_password(password, confirm_password):
                        user_pass = BCRYPT.generate_password_hash(password)
                        query = "INSERT INTO users (email, user_password, driver) \
                                VALUES ('{}', '{}', '{}')".\
                                format(email, password, user_type)
                        cursor.execute(query)
                        conn.commit()
                        conn.close()
                        return {"Status": True, "Message": "Succesfuly created user record"}
                    return {"Status": False, "Message": "Passwords dont match!"}
                return {"Status": False, "Message": "Password should not be less than six characters"}
            return {"Status": False, "Message": "Invalid email Address!"}
        except Exception as e:
            return {"Status": False, "Message": '{}'.format(e)}

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
        if str(password) == str(confirm_password):
            return True

    def find_user(self, connection, email):
        """Retrieve user from db."""
        conn = connection
        cursor = conn.cursor()
        try:
            query = "SELECT * FROM users WHERE Email='{}'".format(email)
            cursor.execute(query)
            rows = cursor.fetchall()
            if rows:
                return {'Status': True, 'Message': rows}
            return {'Status': False, 'Message': 'User not registered'}
        except Exception as e:
            return {'Status': False, 'Message': '{}'.format(e)}


class Ride(object):
    """Handles ride transactions."""

    def create_rides_table(self, connection):
        """Create the table to store rides."""
        conn = connection
        cursor = conn.cursor()
        try:
            query = "CREATE TABLE rides (id serial PRIMARY KEY, \
                                         Destination TEXT, \
                                         Origin TEXT, \
                                         Departure_Time TEXT,\
                                         Departure_Date TEXT, \
                                         Ride_Name TEXT,\
                                         Identifier TEXT,\
                                         No_Plate TEXT, \
                                         Capacity INT, \
                                         Owner_Id INTEGER REFERENCES users(id));"
            print('Error from controler', cursor.execute(query))

            conn.commit()
            conn.close()
            return {'Status': True, 'Message': 'Success!'}
        except Exception as e:
            return {'Status': False, 'Message': '{}'.format(e)}

    def create_ride(self, connection, ride_data):
        """Create a ride."""
        destination = ride_data.get('Destination')
        origin = ride_data.get('Origin')
        departure_time = ride_data.get('Departure Time')
        departure_date = ride_data.get('Departure Date')
        ride_name = ride_data.get('Ride Name')
        identifier = ride_data.get('Identifier')
        no_plate = ride_data.get('No Plate')
        capacity = ride_data.get('Capacity')
        owner_id = ride_data.get('Owner Id')

        if self.find_user(connection, identifier).get('Status'):
            return {'Status': False, 'Message': 'Ride already exists'}
        try:
            conn = connection
            cursor = conn.cursor()
            query = "INSERT INTO rides (destination, origin, departure_time,\
                                 departure_date, ride_name, identifier,\
                                 no_plate, capacity, owner_id)\
                    VALUES ('{}', '{}', '{}', '{}', '{}', '{}', \
                            '{}', '{}', '{}')".\
                    format(destination, origin, departure_time,
                           departure_date, ride_name, identifier,
                           no_plate, capacity, owner_id)
            cursor.execute(query)
            conn.commit()
            conn.close()
            return {"Status": True, "Message": "Succesfuly created ride!"}
        except Exception as e:
            return {"Status": False, "Message": '{}'.format(e)}

    def find_user(self, connection, identifier):
        """Retrieve user from db."""
        conn = connection
        cursor = conn.cursor()
        try:
            query = "SELECT * FROM rides WHERE Identifier='{}'".format(identifier)
            cursor.execute(query)
            rows = cursor.fetchall()
            if rows:
                return {'Status': True, 'Message': rows}
            return {'Status': False, 'Message': 'User not registered'}
        except Exception as e:
            return {'Status': False, 'Message': '{}'.format(e)}
