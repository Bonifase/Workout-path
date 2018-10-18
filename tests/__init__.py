import unittest
import json
from urllib.parse import urljoin
from fhh import app
from config import app_config

from fhh.models.models import *


class BaseTestSetUp(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.app = app
        self.app.config.from_object(app_config['testing'])
        self.app = app.test_client()
        self.testHelper = TestHelper()
        self.base_url = self.testHelper.base_url
        self.app = self.testHelper.app
        self.headers = self.testHelper.headers

        with app.app_context():
            # create all tables
            db.session.close()
            db.drop_all()
            db.create_all()


class TestHelper():

    def __init__(self):
        self.base_url = 'http://127.0.0.1:5000'
        self.headers = {'content-type': 'application/json'}
        self.app = app.test_client()
    # Create a new user

    def add_user(self, user_data):
        url = self.base_url + '/api/user'
        result = self.app.post(url, data=json.dumps(
            user_data), headers=self.headers)
        return result

    def login_user(self, user_data):
        url = self.base_url + '/api/login'
        result = self.app.post(url, data=json.dumps(
            user_data), headers=self.headers)
        return result

    def get_users(self):
        url = self.base_url + '/api/user'
        result = self.app.get(url)
        return result

    def get_user_by_id(self, user_id):
        url = self.base_url + '/api/user/{id}'.format(id=user_id)
        result = self.app.get(url)
        return result

    def change_user_role(self, user_id):
        url = self.base_url + '/api/user/{id}'.format(id=user_id)
        result = self.app.put(url)
        return result

    def delete_user(self, user_id):
        url = self.base_url + '/api/user/{id}'.format(id=user_id)
        result = self.app.delete(url)
        return result

    def update_profile(self, user_id):
        url = self.base_url + '/api/user/{id}'.format(id=user_id)
        result = self.app.put(url)
        return result

    def logout_user(self, token):
        url = self.base_url + '/api/user/logout'
        result = self.app.post()(url)
        return result

    def get_locations(self):
        url = self.base_url + '/api/locations'
        result = self.app.get(url)
        return result
  
    def get_location(self, location_id):
        url = self.base_url + '/api/locations/{id}'.format(id=location_id)
        result = self.app.get(url)
        return result
    
    def add_location(self, user_data):
        url = self.base_url + '/api/location'
        result = self.app.post(url, data=json.dumps(
            user_data), headers=self.headers)
        return result
