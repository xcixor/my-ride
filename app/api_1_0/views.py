"""Implements the endpoints."""

from flask_restful import Resource, reqparse

from flask_jwt_extended import JWTManager

from flask_jwt_extended import create_access_token, jwt_required, get_raw_jwt

from app.api_1_0.controller import Controller

APP_CONTROLLER = Controller()

JWT_MANAGER = JWTManager()


class Signup(Resource):
    """Enables the registration of a user."""

    def __init__(self):
        """Register the parameters to be passed."""
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('Email', type=str,
                                 help='User email is missing', required=True)
        self.parser.add_argument('Password', type=str,
                                 help='User Password is missing',
                                 required=True)
        self.parser.add_argument('Confirm Password', type=str,
                                 help='Confirm Password is missing',
                                 required=True)
        self.parser.add_argument('Type', type=str,
                                 help='Type of user is missing', required=True)
        self.args = self.parser.parse_args()

    def post(self):
        """Send user registration request."""
        user_details = {
            "Email": self.args['Email'],
            "Password": self.args['Password'],
            "Type": self.args['Type'],
            "Confirm Password": self.args['Confirm Password']
        }
        res = APP_CONTROLLER.create_user(user_details)
        if res.get('Status'):
            return {'Message': res.get('Message')}, 201
        return {'Message': res.get('Message')}, 401


class Authenticate(Resource):
    """Handles user authentication."""

    def __init__(self):
        """Register params."""
        self.parser = reqparse.RequestParser()
        self.parser.add_argument(
            'Email', type=str, help='Please provide the email', required=True)
        self.parser.add_argument('Password', type=str,
                                 help='Please provide the password',
                                 required=True)
        self.args = self.parser.parse_args()

    def post(self):
        """Authenticate user with accurate parameters."""
        logins = {
            "Email": self.args['Email'],
            "Password": self.args['Password']
        }
        user = logins['Email']
        if user in APP_CONTROLLER.black_list_token:
            APP_CONTROLLER.black_list_token.pop(user)
        result = APP_CONTROLLER.login(logins)
        if result.get('Status'):
            try:
                token = create_access_token(identity=user)
                return {'Message': 'Successfuly logged in',
                        'access-token': token}, 200
            except Exception as e:
                return {'Status': False,
                        'Message': '{}'.format(e)}, 500
        return {'Message': result.get('Message')}, 403


class Logout(Resource):
    """Logs a user out of their account."""

    @jwt_required
    def post(self):
        """Black list a user session."""
        token = get_raw_jwt().get('access-token')
        user = get_raw_jwt().get('identity')
        APP_CONTROLLER.black_list_token.update({user: token})
        return {'Message': 'Successful logged out'}, 200


class RideCreation(Resource):
    """Handles ride creation."""

    @jwt_required
    def post(self):
        """Create ride."""
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
        parser.add_argument('Time', type=str,
                            help='Please provide the departure time',
                            required=True)
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
        if token not in APP_CONTROLLER.black_list_token.values():
            ride_details.update({'Owner': owner})
            result = APP_CONTROLLER.create_ride(ride_details)
            if result.get('Status'):
                return {'Message': result.get('Message')}, 201
            return {'Message': result.get('Message')}, 401
        return {'Message': 'You are logged out'}, 403

    def get(self):
        """Retrieve all events."""
        result = APP_CONTROLLER.get_rides()
        if result.get('Status'):
            return {'Message': result.get('Message')}, 200
        return {'Message': result.get('Message')}, 404


class RideManipulation(Resource):
    """Performs actions on the ride."""

    @jwt_required
    def get(self, ride_id):
        """Fetch a single event."""
        owner = get_raw_jwt().get('identity')
        token = get_raw_jwt().get('access-token')
        if token not in APP_CONTROLLER.black_list_token.values():
            result = APP_CONTROLLER.get_ride(owner, ride_id)
            if result.get('Status'):
                return{'Message': result.get('Message')}, 200
            return {'Message': result.get('Message')}, 404
        return {'Message': 'You are logged out'}, 403

    @jwt_required
    def put(self, ride_id):
        """Edit ride details."""
        parser = reqparse.RequestParser()
        parser.add_argument('Ride Name', type=str,
                            help='Please provide name of your vehicle',
                            required=False)
        parser.add_argument('Capacity', type=str,
                            help='Please provide number of people it carries',
                            required=False)
        parser.add_argument('Origin', type=str,
                            help='Please the starting point',
                            required=False)
        parser.add_argument('Destination', type=str,
                            help='Please provide your destination',
                            required=False)
        parser.add_argument('Date', type=str, help='Please provide the date',
                            required=False)
        parser.add_argument('Time', type=str,
                            help='Please provide the departure time',
                            required=False)
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
        if token not in APP_CONTROLLER.black_list_token.values():
            result = APP_CONTROLLER.edit_ride(ride_id, owner, new_details)
            if result.get('Status'):
                return {'Message': result.get('Message')}, 201
            return {'Message': result.get('Message')}, 400
        return {'Message': 'You have already logged out'}, 403


class RideRequests(Resource):
    """handles ride request."""

    @jwt_required
    def post(self, ride_id):
        """Create a ride request."""
        requester = get_raw_jwt().get('identity')
        details = {"Email": requester}
        result = APP_CONTROLLER.make_request(ride_id, details)
        if result.get('Status'):
            return {'Message': result.get('Message')}, 200
        return {'Message': result.get('Message')}, 400
