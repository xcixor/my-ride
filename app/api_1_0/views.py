"""Implements the endpoints."""
from app.api_1_0.controller import Controller

from flask_restful import Resource, reqparse

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
            return res.get('Message'), 201
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

    def post (self):
        """Authenticate user with accurate parameters."""
        logins = {
            "Email": self.args['Email'],
            "Password": self.args['Password']
        }
        result = app_controller.login(logins)
        if result.get('Status'):
            return result.get('Message'), 201
        else:
            return result.get('Message'), 403
