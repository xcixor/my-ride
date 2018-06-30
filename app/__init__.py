"""Initialize the application."""
from flask import Flask
from flask_restful import Api
from config import config
from app.api_1_0 import views
from app.api_1_0.views import JWT_MANAGER
from app.api_1_0 import api_v1

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

    #Register blueprints
    app.register_blueprint(api_v1, url_prefix='/api/v1')
    return app
