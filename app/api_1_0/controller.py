"""Facilitates communication between the views and the models."""
from app.api_1_0.models import AppUser


class Controller(object):
    """Manipulates the model functionality."""

    def __init__(self):
        """Initialize objects."""
        self.user = AppUser()

    def create_user(self, user_details):
        """Create a user for the application."""
        # try:
        email = user_details.get('Email')
        user_type = user_details.get('Type')
        password = user_details.get('Password')
        confirm_password = user_details.get('Confirm Password')
        # except KeyError as e:
        #     raise Exception("{} is required but is missing".format((e))) from e
        # else:
        user_id = Controller.generate_id(self.user.app_users)
        user_data = {'Email': email, 'Password': password, "Type": user_type, 'Confirm Password': confirm_password, 'Id': user_id}
        result = self.user.create_user(user_data)
        if result.get('Status'):
            return {'Status': True, 'Message': result.get('Message')}
        else:
            return {'Status': False, 'Message': result.get('Message')}

    @staticmethod
    def generate_id(item_data, item_id=0):
        """Create an id from the list of items provided.

        Args:
            items(iterable object)obejct from which id is determined.
            item_id(int): Initial id
        """
        if item_id == 0:
            item_id = len(item_data) + 1
        for key, value in item_data.items():
            if value['Id'] == item_id:
                item_id += 1
                Controller.generate_id(item_data, item_id)
        return item_id

# if __name__ == '__main__':
#     controller = Controller()
#     user_data = {
#            "Email": "wama@gmail.com",
#            "Password": "pass123",
#            "Confirm Password": "pass123"
#        }
#     user_data2 = {
#            "Email": "wami@gmail.com",
#            "Password": "pass123",
#            "Confirm Password": "pass123"
#        }
#     user_data3 = {
#         "Email": "wamai@gmail.com",
#         "Password": "pass123",
#         "Confirm Password": "pass123"
#     }
#     controller.create_user(user_data)
#     controller.create_user(user_data2)
#     controller.create_user(user_data3)
#     # for item in controller.user.app_users:
#     #     print(item.items())
#     # for key, value in controller.user.app_users.items():
#     #     print(value.get('Email'))
#     print(controller.generate_id(controller.user.app_users))
#     # print(controller.user.app_users)
