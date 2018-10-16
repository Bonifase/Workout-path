import unittest
import json
from tests import BaseTestSetUp
from tests.data import *


class TestUserCase(BaseTestSetUp):

    def test_new_user_registration_works(self):
        """Test API registers new user successfully (POST request)"""

        response = self.testHelper.add_user(new_user)
        result = json.loads(response.data.decode())
        self.assertEqual(result[
            "message"], new_user['first_name'] + " created")
        self.assertEqual(response.status_code, 201)

    def test_user_login_works(self):
        """Test API logs in users successfully (POST request)"""

        self.testHelper.add_user(user_data)
        response = self.testHelper.login_user(user_data)
        result = json.loads(response.data.decode())
        self.assertEqual(result["message"], "You logged in successfully.")
    
    def test_wrong_email_login_fails(self):
        """Test API rejects wrong email during login (POST request)"""

        response = self.testHelper.login_user(wrong_email)
        result = json.loads(response.data.decode())
        self.assertEqual(result["message"], "User not found")

    def test_unregistered_user_login_fails(self):
        """Test API rejects unregistered users login (POST request)"""

        response = self.testHelper.login_user(unregistered_user)
        result = json.loads(response.data.decode())
        self.assertEqual(result["message"], "User not found")
