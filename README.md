[![Build Status](https://travis-ci.org/xcixor/my-ride.svg?branch=158619400-edit-ride)](https://travis-ci.org/xcixor/my-ride)
[![Maintainability](https://api.codeclimate.com/v1/badges/80451ea43faa9ca7b80d/maintainability)](https://codeclimate.com/github/xcixor/my-ride/maintainability)
[![Coverage Status](https://coveralls.io/repos/github/xcixor/my-ride/badge.svg?branch=158619400-edit-ride)](https://coveralls.io/github/xcixor/my-ride?branch=158619400-edit-ride)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/c0fe78ccda6444e9baef4265469e29e8)](https://www.codacy.com/app/xcixor/my-ride?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=xcixor/my-ride&amp;utm_campaign=Badge_Grade)

## Purpose
ride-my-way App is a carpooling application that provides drivers with the ability to create ride offers and passengers to join available ride offers

## Preliquisites
* [python 3*](https://www.python.org/downloads/)
* [Git](https://git-scm.com/)
* [Virtual env](https://virtualenv.pypa.io/en/stable/)

## Development
* Navigate to the repo's main page via  [this link](https://github.com/xcixor/my-ride)
* Under the repo's name copy the clone's url
* Open a terminal and navigate to where you want the repo to be downloaded
* Type git clone 'the url you copied above' and press enter to download
* Set up a virtual env and install the dependencies in requirements.txt
* Checkout to the branch 158619400-edit-ride
* Run the run.py file to start the server
* Make the following requests using postman
### endpoints
|Resource urls                                    | Method     | Description               | Requires token  |
|-------------------------------------------------|------------|---------------------------|-----------------|
| /api/v1/auth/register                           |   POST     | Register a user           |    FALSE        |
| /api/v1/auth/login                              |   POST     | Login user                |    FALSE        |
| /api/v1/rides                                   |   POST     | Create ride               |    TRUE         |
| /api/v1/ride/&lt;ride_id&gt;                    |   PUT      | Update ride details       |    TRUE         |
| /api/v1/rides                                   |   GET      | Retrieve rides            |    FALSE        |
| /api/v1/rides/&lt;ride_id&gt;                   |   GET      | Retrieve a ride           |    TRUE         |
| /api/v1/ride/&lt;ride_id&gt;/requests       |   POST     | Request a ride            |    TRUE         |

* From there build on this app

## Documentation
You can view the documentation of the api at [apiary](https://myride.docs.apiary.io/#)

## Deployment
my-ride is hosted at [heroku]( https://my-ride.herokuapp.com/)

## Built with
#### Backend
* flask
* flask_restful
* python
## Contributing
My friends at andela 21
## Version
my-ride 1.0
## Licenses
None
#### Front end
* css
* html
* js

You can preview the frontend via this [link](https://xcixor.github.io/my-ride)
