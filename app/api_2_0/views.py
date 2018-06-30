"""Api endpoints implementation."""
from flask_restful import Resource, reqparse
from app.api_2_0.models import User

USER = User()


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

        resp = USER.create_user(email, password, confirm_password, user_type)
        if resp.get('Status'):
            return {'Status': True, 'Message': 'User successfuly created'}
        return {'Status': True, 'Message': resp.get('Message')}, 201
