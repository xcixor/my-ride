"""Contains tests for api endpoints."""

import unittest
import json
from app import create_app
import flask
from flask import session, request
import requests
from unittest.mock import patch


class TestApi(unittest.TestCase):
    """Tests the api endpoints."""

    def setUp(self):
        """Initialize objects for the tests."""
        self.driver = {
            "Email": "p@gmail.com",
            "Type": "driver",
            "Password": "pass123",
            "Confirm Password": "pass123"
        }
        self.ride = {
            "Destination": "Meru",
            "Origin": "Kutus",
            "Time": "9:00",
            "Date": "23-6-2018",
            "Ride Name": "Toyota",
            "Capacity": "7"
        }
        self.request = {
            "Email": "Njobu",
            "Tel": "+254716272376"
        }
        self.app = create_app('testing')
        self.client = self.app.test_client
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        """Remove objects after test."""
        self.app_context.pop()

    def test_create_ride_if_signed_in_success(self):
        # signup
        user = {
            "Email": "m@g.com",
            "Type": "passenger",
            "Password": "pass234",
            "Confirm Password": "pass234"
        }

        response = self.client().post('/api/v1/auth/register',
                                      data=user)
        self.assertEqual(response.status_code, 201)

        # login
        logins = {"Email": "m@g.com", "Password": "pass234"}
        res = self.client().post('api/v1/auth/login', data=logins)
        self.assertEqual(res.status_code, 200)

        # get authorization token
        token = json.loads(res.data.decode('UTF-8'))
        access_token = token.get('access-token')

        # create ride
        res = self.client().post('/api/v1/rides',
                                data=self.ride,
                                headers={'Authorization': 'Bearer '+access_token})
        self.assertEqual(res.status_code, 201)

    def test_register_user_with_correct_credentials_success(self):
        """Test user can register successfuly with correct credentials."""
        response = self.client().post('/api/v1/auth/register',
                                      data=self.driver)
        self.assertEqual(response.status_code, 201)

    def test_login_with_correct_authentication_success(self):
        """Test user can login with correct credentials."""
        user = {
            "Email": "fyi@g.com",
            "Type": "passenger",
            "Password": "pass234",
            "Confirm Password": "pass234"
        }
        response = self.client().post('/api/v1/auth/register',
                                      data=user)
        self.assertEqual(response.status_code, 201)
        logins = {"Email": "fyi@g.com", "Password": "pass234"}
        res = self.client().post('/api/v1/auth/login', data=logins)
        self.assertTrue(res.status_code, 200)

    def test_login_without_registration_false(self):
        """Test an unregistered user cannot log in."""
        logins = {"email": "esta@x.com", "Password": "pass234"}
        res = self.client().post('/api/v1/auth/login', data=logins)
        self.assertTrue(res.status_code, 403)

    def test_edit_ride_if_signed_in_success(self):
        """Test user can edit a ride."""
        # signup
        passenger = {
            "Email": "may@yahoo.com",
            "Type": "passenger",
            "Password": "pass234",
            "Confirm Password": "pass234"
        }

        response = self.client().post('/api/v1/auth/register',
                                          data=passenger)
        self.assertEqual(response.status_code, 201)

        # # login
        logins = {"Email": "may@yahoo.com", "Password": "pass234"}
        res = self.client().post('api/v1/auth/login', data=logins)
        self.assertEqual(res.status_code, 200)

        # # get authorization token
        token = json.loads(res.data.decode('UTF-8'))
        access_token = token.get('access-token')

        # edit the ride
        edit_data = {"Ride Name": "Red", "Capacity": 7}
        res = self.client().put('/api/v1/rides/1', data=edit_data,
                                headers={'Authorization': 'Bearer '+access_token})
        self.assertEqual(res.status_code, 200)

    def test_get_ride_if_exists_success(self):
        """Test user can get a ride successfuly."""
        ride = {
            "Destination": "Meru",
            "Origin": "Kutus",
            "Time": "8:00",
            "Date": "25-6-2018",
            "Ride Name": "Toyota",
            "Capacity": "7"
        }
        passenger = {
            "Email": "yu@hu.com",
            "Type": "passenger",
            "Password": "pass234",
            "Confirm Password": "pass234"
        }
        res = self.client().post('/api/v1/auth/register', data=passenger)
        self.assertEqual(res.status_code, 201)
        logins = {
            "Email": "yu@hu.com",
            "Password": "pass234"
        }
        response = self.client().post('/api/v1/auth/login', data=logins)
        self.assertEqual(response.status_code, 200)
        token = json.loads(response.data.decode('UTF-8'))
        access_token = token.get('access-token')

        res = self.client().post('/api/v1/rides',
                                        data=ride,
                                        headers={'Authorization': 'Bearer '+access_token})
        self.assertEqual(res.status_code, 201)

    def test_get_all_rides_if_exists_success(self):
        """Test get all rides offers successfuly."""
        res = self.client().get('api/v1/rides')
        self.assertEqual(res.status_code, 200)
        self.assertIn('Kutus', str(res.data))

    def test_make_ride_request_if_signed_in_success(self):
        """Test user can make a request successfuly."""
        # signup
        passenger = {
            "Email": "dru@gmail.com",
            "Type": "passenger",
            "Password": "pass234",
            "Confirm Password": "pass234"
        }
        res = self.client().post('/api/v1/auth/register', data=passenger)
        self.assertEqual(res.status_code, 201)
        # login
        logins = {"Email": "dru@gmail.com", "Password": "pass234"}
        res = self.client().post('api/v1/auth/login', data=logins)
        self.assertEqual(res.status_code, 200)

        # get authorization token
        token = json.loads(res.data.decode('UTF-8'))
        access_token = token.get('access-token')

        # request ride
        res = self.client().post('api/v1/rides/1/requests', data=self.request,
                                 headers={'Authorization': 'Bearer '+access_token})
        self.assertEqual(res.status_code, 200)

    def test_logout_success(self):
        # signup
        passenger = {
            "Email": "trump@hotmail.com",
            "Type": "passenger",
            "Password": "pass234",
            "Confirm Password": "pass234"
        }
        res = self.client().post('/api/v1/auth/register', data=passenger)
        self.assertEqual(res.status_code, 201)
        # login
        logins = {"Email": "trump@hotmail.com", "Password": "pass234"}
        res = self.client().post('api/v1/auth/login', data=logins)
        self.assertEqual(res.status_code, 200)

        # get authorization token
        token = json.loads(res.data.decode('UTF-8'))
        access_token = token.get('access-token')

        # logout
        res = self.client().post('api/v1/auth/logout', headers={'Authorization': 'Bearer '+access_token})
        self.assertEqual(res.status_code, 200)
