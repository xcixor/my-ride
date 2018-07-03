"""Contains app configurations."""

import os


class Config:
    """Contains the basic settings for all configurations."""

    debug = False
    SECRET_KEY = os.urandom(30)
    SECRET_KEY = "A very secretive key"


    @staticmethod
    def init_app(app):
        """To perform configuration specific initializations."""
        pass


class Development(Config):
    """Contains configurations to be used by developer."""

    DEBUG = True
    db_url = os.environ.get('Production_database_url') or "dbname='rides_production' user='rider' \
        password='pass123' host='localhost' port='5432'"
    db = {
        "dbname": "rides",
        "user": "rider",
        "password": "pass123",
        "host": "localhost",
        "port": "5432"
    }


class Testing(Config):
    """Contains configurations for testing."""

    TESTING = True
    db = {
        "dbname": "rides_test",
        "user": "rider",
        "password": "pass123",
        "host": "localhost",
        "port": "5432"
    }


class Production(Config):
    """Contains configurations for production setting."""

    DEBUG = False
    db = {
        "dbname": "rides",
        "user": "rider",
        "password": "pass123",
        "host": "localhost",
        "port": "5432"
    }

# Registers the configurations
config = {
    'development': Development,
    'testing': Testing,
    'production': Production,
    'default': Development
}
