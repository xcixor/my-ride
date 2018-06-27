"""Initialize the application."""
from flask import Flask
from flask_restful import Api
from config import config
from app.api_1_0 import views
from app.api_1_0.views import JWT_MANAGER

def create_app(configuration):
    """Set up the application.

    args:
        configuration(str): The name of the configuration type to use for
        app instance

    returns:
        app(object): application instance

    """

    # initialize app with api
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config[configuration])
    config[configuration].init_app(app)
    JWT_MANAGER.init_app(app)

    api = Api(app)

    # define routes
    api.add_resource(views.Signup, '/api/v1/auth/register')
    api.add_resource(views.Authenticate, '/api/v1/auth/login')
    api.add_resource(views.RideCreation, '/api/v1/rides')
    api.add_resource(views.RideManipulation, '/api/v1/rides/<ride_id>')
    api.add_resource(views.RideRequests, '/api/v1/rides/<ride_id>/requests')
    api.add_resource(views.Logout, '/api/v1/auth/logout')
    return app
