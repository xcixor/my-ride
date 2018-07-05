# define routes
from app.api_2_0 import api
from app.api_2_0 import views

api.add_resource(views.UserSignup, '/auth/register')
api.add_resource(views.UserLogin, '/auth/login')
api.add_resource(views.CreateRide, '/rides')
api.add_resource(views.ManipulateRides, '/rides/<ride_id>')
api.add_resource(views.Requests, '/rides/<ride_id>/requests')
api.add_resource(views.ManageRequests, '/users/rides/<ride_id>/requests')
api.add_resource(views.RequestStatus, '/users/rides/<ride_id>/requests/<request_id>')
