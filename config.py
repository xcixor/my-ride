"""Contains app configurations."""

import os


class Config:
    """Contains the basic settings for all configurations."""

    debug = False
    SECRET_KEY = os.urandom(30)

    @staticmethod
    def init_app(app):
        """To perform configuration specific initializations."""
        pass


class Development(Config):
    """Contains configurations to be used by developer."""

    DEBUG = True


class Testing(Config):
    """Contains configurations for testing."""

    TESTING = True


class Production(Config):
    """Contains configurations for production setting."""

    DEBUG = False


# Registers the configurations
config = {
    'development': Development,
    'testing': Testing,
    'production': Production,
    'default': Development
}
