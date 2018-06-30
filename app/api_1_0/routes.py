# define routes
from app.api_1_0 import api
from app.api_1_0 import views

api.add_resource(views.Signup, '/auth/register')
api.add_resource(views.Authenticate, '/auth/login')
api.add_resource(views.RideCreation, '/rides')
api.add_resource(views.RideManipulation, '/rides/<ride_id>')
api.add_resource(views.RideRequests, '/rides/<ride_id>/requests')
api.add_resource(views.Logout, '/auth/logout')
