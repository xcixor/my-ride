"""Contains the classes for modelling the application."""
import re


class AppUser(object):
    """Handles user functionality."""

    def __init__(self):
        """Initialize an instance of the User class.

        Args:
            users(dict): Contains user records.
        """
        self.app_users = {}

    def create_user(self, user_details):
        """Register a new user.

        Args:
            user_details(dict): User details
        """
        email = user_details.get('Email')
        password = user_details.get('Password')
        confirm_password = user_details.get('Confirm Password')
        if email in self.app_users:
            return {"Status": False, "Message": "That user already exists"}
        elif not AppUser.verify_password_length(password):
            return {"Status": False, "Message": "Password should not be less than six characters!"}
        elif not AppUser.verify_email(email):
            return {"Status": False, "Message": "Invalid email address!"}
        elif not password == confirm_password:
            return {"Status": True, "Message": "Passwords do not match!"}
        else:
            user = {email: user_details}
            self.app_users.update(user)
            return {"Status": True, "Message": "Successfuly Created account"}

    @staticmethod
    def verify_email(email):
        """Check if email adress is valid.

        Returns:
        True if email is valid.

        """
        if re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",
                    email):
            return True

    @staticmethod
    def verify_password_length(password):
        """Check password is valid.

        Returns:
        True if password is long enough.

        """
        if len(password) >= 6:
            return True

    def get_user(self, email):
        """Retrieves a user from the users records.

        Returns user(dict):
        """
        if email in self.app_users:
            return {'Status': True, 'Message': self.app_users.get(email)}
        else:
            return {'Status': False, 'Message': 'That user does not exist'}

    def login(self, email, password):
        """Check if credentials are correct to allow login."""
        res = self.get_user(email)
        print('&&&&&&&&&&&&&&&&&&&&&&', res.get('Message'))
        if res.get('Status'):
            if password == res.get('Message').get('Password'):
                return {'Status': True, 'Message': 'Login Successful'}
            else:
                return {'Status': False, 'Message': 'Password incorrect!'}
        else:
            return {'Status': True, 'Message': 'User does not exist'}
