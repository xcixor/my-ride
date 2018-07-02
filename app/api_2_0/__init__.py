
"""Initializes the api v2 blueprint."""
from flask import Blueprint
from flask_restful import Api

api_v2 = Blueprint('api_v2', __name__)

api = Api(api_v2)

from . import routes
