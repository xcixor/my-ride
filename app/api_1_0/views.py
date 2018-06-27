"""Implements the endpoints."""
from app.api_1_0.controller import Controller

from flask_restful import Resource, reqparse

from flask import session, current_app, request, jsonify

from functools import wraps

from flask_jwt_extended import JWTManager

from flask import jsonify

from datetime import datetime, timedelta

app_controller = Controller()

from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_raw_jwt

jwt_manager = JWTManager()

black_list = {}

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
        user = logins['Email']
        result = app_controller.login(logins)
        if result.get('Status'):
            try:
                token = create_access_token(identity=user)
                status_code = 200
                return {'Status': True, 'access-token': token}, status_code
            except:
                return {'Status': False, 'Message': 'Token could not be creted at this point'}, 500
        else:
            return {'Status': False, 'Message': result.get('Message')}


class Logout(Resource):
    """Logs a user out of their account."""
    @jwt_required
    def post(self):
        token = get_raw_jwt().get('access-token')
        user = get_raw_jwt().get('identity')
        status_code = 200
        app_controller.black_list_token.update({user:token})
        return {'Message': 'Successful logged out'}, status_code


class RideCreation(Resource):
    """Handles ride creation."""

    def __init__(self):
        """Register params."""
        pass

    @jwt_required
    def post(self):
        """Create ride."""
        parser = reqparse.RequestParser()
        parser.add_argument('Ride Name', type=str, help='Please provide name of your vehicle', required=True)
        parser.add_argument('Capacity', type=str, help='Please provide number of people it carries', required=True)
        parser.add_argument('Origin', type=str, help='Please the starting point', required=True)
        parser.add_argument('Destination', type=str, help='Please provide your destination', required=True)
        parser.add_argument('Date', type=str, help='Please provide the date', required=True)
        parser.add_argument('Time', type=str, help='Please provide the departure time', required=True)
        args = parser.parse_args()
        ride_details = {
            "Ride Name": args.get('Ride Name'),
            "Capacity": args.get('Capacity'),
            "Origin": args.get('Origin'),
            "Destination": args.get('Destination'),
            "Date": args.get('Date'),
            "Time": args.get('Time')
        }
        owner = get_raw_jwt().get('identity')
        token = get_raw_jwt().get('access-token')
        if token not in app_controller.black_list_token.values():
            ride_details.update({'Owner': owner})
            result = app_controller.create_ride(ride_details)
            if result.get('Status'):
                status_code = 201
                return result.get('Message'), status_code
            else:
                status_code = 401
                return result.get('Message'), status_code
        else:
            status_code = 403
            return {'Status': False, 'Message': 'You have already been logged out login to create rides'}, status_code

    def get(self):
        """Retrieve all events."""
        result = app_controller.get_rides()
        if result.get('Status'):
            status_code = 200
            return result.get('Message'), status_code
        else:
            status_code = 404
            return result.get('Message'), status_code


class RideManipulation(Resource):
    """Performs actions on the ride."""

    @jwt_required
    def get(self, ride_id):
        """Fetch a single event."""
        owner = get_raw_jwt().get('identity')
        token = get_raw_jwt().get('access-token')
        if token not in app_controller.black_list_token.values():
            result = app_controller.get_ride(owner, ride_id)
            if result.get('Status'):
                status_code = 200
                return result.get('Message'), status_code
            else:
                status_code = 404
                return result.get('Message'), status_code
        else:
            status_code = 403
            return {'Status': False, 'Message': 'You have already been logged out login to get your ride'}, status_code

    @jwt_required
    def put(self, ride_id):
        parser = reqparse.RequestParser()
        parser.add_argument(
            'Ride Name', type=str, help='Please provide name of your vehicle', required=False)
        parser.add_argument(
            'Capacity', type=str, help='Please provide number of people it carries', required=False)
        parser.add_argument(
            'Origin', type=str, help='Please the starting point', required=False)
        parser.add_argument(
            'Destination', type=str, help='Please provide your destination', required=False)
        parser.add_argument(
            'Date', type=str, help='Please provide the date', required=False)
        parser.add_argument(
            'Time', type=str, help='Please provide the departure time', required=False)
        args = parser.parse_args()
        details = {
            "Ride Name": args.get('Ride Name'),
            "Capacity": args.get('Capacity'),
            "Origin": args.get('Origin'),
            "Destination": args.get('Destination'),
            "Date": args.get('Date'),
            "Time": args.get('Time')
        }
        new_details = {}
        for key, value in details.items():
            if details[key]:
                new_details[key] = value
        owner = get_raw_jwt().get('identity')
        token = get_raw_jwt().get('access-token')
        if token not in app_controller.black_list_token.values():
            result = app_controller.edit_ride(ride_id, owner, new_details)
            if result.get('Status'):
                status_code = 201
                return result.get('Message'), status_code
            else:
                status_code = 409
                return
        else:
            status_code = 403
            return {'Status': False, 'Message': 'You have already been logged out login to edit your ride'}, status_code


class RideRequests(Resource):
    """Performs actions on the ride."""

    @jwt_required
    def post(self, ride_id):
        parser = reqparse.RequestParser()
        parser.add_argument(
            'Email', type=str, help='Please provide your email', required=True)
        args = parser.parse_args()
        details = {
            "Email": args.get('Email')
        }
        owner = get_raw_jwt().get('identity')
        result = app_controller.make_request(ride_id, owner, details)
        if result.get('Status'):
            status_code = 200
            return result.get('Message'), status_code
        else:
            status_code = 409
            return
