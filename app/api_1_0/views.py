"""Implements the endpoints."""
from app.api_1_0.controller import Controller

from flask_restful import Resource, reqparse

from flask import session

from functools import wraps

app_controller = Controller()


class Signup(Resource):
    """Enables the registration of a user."""

    def __init__(self):
        """Register the parameters to be passed."""
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('Email', type=str, help='User email is missing', required=True)
        self.parser.add_argument(
            'Password', type=str, help='User Password is missing', required=True)
        self.parser.add_argument(
            'Confirm Password', type=str, help='Confirm Password is missing', required=True)
        self.parser.add_argument(
             'Type', type=str, help='Type of user is missing', required=True)
        self.args = self.parser.parse_args()

    def post(self):
        """Send user registration request."""
        user_details = {
            "Email": self.args['Email'],
            "Password": self.args['Password'],
            "Type": self.args['Type'],
            "Confirm Password": self.args['Confirm Password']
        }
        res = app_controller.create_user(user_details)
        if res.get('Status'):
            status_code = 201
            return res.get('Message'), status_code
        else:
            return res.get('Message'), 401


def authentication_required(function):
    """Check whether user is logged in before proceeding."""
    @wraps(function)
    def authenticate(*args, **kwargs):
        """Check if user has a session."""
        if not session['logged_in']:
            return {'Status': False, 'Message': 'You need to be logged in'}, 403
        return function(*args, **kwargs)
    return authenticate


class Authenticate(Resource):
    """Handles user authentication."""

    def __init__(self):
        """Register params."""
        self.parser = reqparse.RequestParser()
        self.parser.add_argument(
            'Email', type=str, help='Please provide the email', required=True)
        self.parser.add_argument(
            'Password', type=str, help='Please provide the password', required=True)
        self.args = self.parser.parse_args()

    def post(self):
        """Authenticate user with accurate parameters."""
        logins = {
            "Email": self.args['Email'],
            "Password": self.args['Password']
        }
        result = app_controller.login(logins)
        if result.get('Status'):
            session['user'] = self.args['Email']
            session['logged_in'] = True
            status_code = 201
            return result.get('Message'), status_code
        else:
            status_code = 403
            return result.get('Message'), status_code


class RideCreation(Resource):
    """Handles ride creation."""

    def __init__(self):
        """Register params."""
        self.parser = reqparse.RequestParser()
        self.parser.add_argument(
            'Ride Name', type=str, help='Please provide name of your vehicle', required=True)
        self.parser.add_argument(
            'Capacity', type=str, help='Please provide number of people it carries', required=True)
        self.parser.add_argument(
            'Origin', type=str, help='Please the starting point', required=True)
        self.parser.add_argument(
            'Destination', type=str, help='Please provide your destination', required=True)
        self.parser.add_argument(
            'Date', type=str, help='Please provide the date', required=True)
        self.parser.add_argument(
            'Time', type=str, help='Please provide the departure time', required=True)
        self.args = self.parser.parse_args()


    @authentication_required
    def post(self):
        """Create ride."""
        ride_details = {
            "Ride Name": self.args.get('Ride Name'),
            "Capacity": self.args.get('Capacity'),
            "Origin": self.args.get('Origin'),
            "Destination": self.args.get('Destination'),
            "Date": self.args.get('Date'),
            "Time": self.args.get('Time')
        }
        owner = session['user']
        ride_details.update({'Owner': owner})
        result = app_controller.create_ride(ride_details)
        if result.get('Status'):
            status_code = 201
            return result.get('Message'), status_code
        else:
            status_code = 401
            return result.get('Message'), status_code
