"""Contains code that defines the api_v1 blueprint."""
from flask import Blueprint

api = Blueprint('api', __name__)

from app.api_1_0 import views
