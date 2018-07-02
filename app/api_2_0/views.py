"""Api endpoints implementation."""
from flask_restful import Resource, reqparse
from app.api_2_0.controller import Controller

CONTROLLER = Controller()

class Signup(Resource):
    """Creates a user record."""

    def __init__(self):
        """Initialize params."""
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('Email', type=str,
                                 help='Please provide your email', required=True)
        self.parser.add_argument('Password', type=str,
                                 help='Please provide a password',
                                 required=True)
        self.parser.add_argument('Confirm Password', type=str,
                                 help='Your must confirm your password',
                                 required=True)
        self.parser.add_argument('Type', type=str,
                                 help='Type of user is missing', required=True)
        self.args = self.parser.parse_args()

    def post(self):
        """Resgister user."""
        email = self.args['Email'],
        password = self.args['Password'],
        user_type = self.args['Type'],
        confirm_password = self.args['Confirm Password']
        driver = False
        if user_type[0] == 'driver':
            driver = True
        user_data = {
            "Email": email[0],
            "Password": password[0],
            "Confirm Password": confirm_password,
            "Type": driver
        }
        resp = CONTROLLER.create_user(user_data)
        if resp.get('Status'):
            return {'Message': resp.get('Message')}, 201
        return {'Message': resp.get('Message')}, 400
