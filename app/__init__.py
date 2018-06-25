"""Initialize the application."""
from flask import Flask
from flask_restful import Api
from flask_api import FlaskAPI
from config import config
from app.api_1_0 import views


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
    api = Api(app)

    # define routes
    api.add_resource(views.Signup, '/api/v1/auth/register')


    return app
