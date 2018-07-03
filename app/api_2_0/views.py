"""Api endpoints implementation."""
from flask_restful import Resource, reqparse
from app.api_2_0.controller import Controller
from flask_jwt_extended import JWTManager

from flask_jwt_extended import create_access_token, jwt_required, get_raw_jwt

CONTROLLER = Controller()
JWT_MANAGER = JWTManager()

class UserSignup(Resource):
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


class UserLogin(Resource):
    """Logs in user to their account."""

    def __init__(self):
        """Initialize parameters."""
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('Email', type=str,
                                 help='Please provide your email', required=True)
        self.parser.add_argument('Password', type=str,
                                 help='Please provide a password',
                                 required=True)
        self.args = self.parser.parse_args()

    def post(self):
        """Send user logins."""
        email = self.args['Email']
        password = self.args['Password']
        logins = {
            "Email": email,
            "Password": password
        }
        resp = CONTROLLER.verify_user_credentials(logins)
        if resp.get('Status'):
            try:
                access_token = create_access_token(identity=email)
                return {'Message': 'Successfuly logged in',
                        'access-token': access_token}, 200
            except Exception as e:
                return {'Status': False,
                        'Message': '{}'.format(e)}, 500
        return {'Message': resp.get('Message')}, 403


class CreateRide(Resource):
    """Create rides."""

    @jwt_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('Ride Name', type=str,
                            help='Please provide name of your vehicle',
                            required=True)
        parser.add_argument('Capacity', type=str,
                            help='Please provide number of people it carries',
                            required=True)
        parser.add_argument('Origin', type=str,
                            help='Please the starting point',
                            required=True)
        parser.add_argument('Destination', type=str,
                            help='Please provide your destination',
                            required=True)
        parser.add_argument('Date', type=str,
                            help='Please provide the date',
                            required=True)
        parser.add_argument('Date', type=str,
                            help='Please provide the date',
                            required=True)
        parser.add_argument('No Plate', type=str,
                            help='Please provide the departure time',
                            required=False)
        args = parser.parse_args()

        owner = get_raw_jwt().get('identity')
        ride_details = {
            "Ride Name": args.get('Ride Name'),
            "Capacity": args.get('Capacity'),
            "Origin": args.get('Origin'),
            "Destination": args.get('Destination'),
            "Date": args.get('Date'),
            "Time": args.get('Time'),
            "No Plate": args.get('No Plate'),
            "Owner": owner
        }
        res = CONTROLLER.create_ride(ride_details)
        if res.get('Status'):
            return {'message': res.get('Message')}, 201
        return {'message': res.get('Message')}, 400
