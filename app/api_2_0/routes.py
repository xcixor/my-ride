# define routes
from app.api_2_0 import api
from app.api_2_0 import views

api.add_resource(views.Signup, '/auth/register')
