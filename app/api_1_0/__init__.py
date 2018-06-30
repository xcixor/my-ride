
"""Initializes the api v1 blueprint."""
from flask import Blueprint
from flask_restful import Api

api_v1 = Blueprint('api_v1', __name__)

api = Api(api_v1)

from . import routes
