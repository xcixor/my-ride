# define routes
from app.api_2_0 import api
from app.api_2_0 import views

api.add_resource(views.UserSignup, '/auth/register')
api.add_resource(views.UserLogin, '/auth/login')
api.add_resource(views.CreateRide, '/users/rides')
api.add_resource(views.ManipulateRides, '/rides/<int:ride_id>')
api.add_resource(views.Requests, '/rides/<int:ride_id>/requests')
api.add_resource(views.ManageRequests, '/users/rides/<int:ride_id>/requests')
api.add_resource(views.RequestStatus,
                 '/users/rides/<int:ride_id>/requests/<int:request_id>')
