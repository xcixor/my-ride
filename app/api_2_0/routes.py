# define routes
from app.api_2_0 import api
from app.api_2_0 import views

api.add_resource(views.UserSignup, '/auth/register')
api.add_resource(views.UserLogin, '/auth/login')
api.add_resource(views.CreateRide, '/rides')
