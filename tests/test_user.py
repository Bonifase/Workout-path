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
        add_user = self.testHelper.add_user(new_user)
        self.testHelper.add_user(user_data)
        response = self.testHelper.login_user(wrong_email)
        result = json.loads(response.data.decode())
        self.assertEqual(result["message"], "User not found")

    def test_wrong_password_login_fails(self):
        """Test API rejects wrong password during login (POST request)"""
        add_user = self.testHelper.add_user(new_user)
        self.testHelper.add_user(user_data)
        response = self.testHelper.login_user(wrong_password)
        result = json.loads(response.data.decode())
        self.assertEqual(result["message"], "Wrong Password")

    def test_unregistered_user_login_fails(self):
        """Test API rejects unregistered users login (POST request)"""
        add_user = self.testHelper.add_user(new_user)
        response = self.testHelper.login_user(unregistered_user)
        result = json.loads(response.data.decode())
        self.assertEqual(result["message"], "User not found")

    def test_get_all_users_works(self):
        """Test API get all users (GET request)"""

        response = self.testHelper.get_users()
        result = json.loads(response.data.decode())
        self.assertEqual(result["message"], "There are no users")
    
    def test_get_all_users_works(self):
        """Test API get all users work (GET request)"""
        add_user = self.testHelper.add_user(new_user)
        response = self.testHelper.get_users()
        result = json.loads(response.data.decode())
        self.assertEqual(
            result["users"][0]['first_name'], new_user['first_name'])

    def test_get_user_by_id(self):
        """Test API get user by ID (GET request)"""
 
        response = self.testHelper.get_user_by_id(user_id=1)
        result = json.loads(response.data.decode())
        self.assertEqual(result["message"], "User not found")

    def test_get_user_by_id(self):
        """Test API get user by ID (GET request)"""
        add_user = self.testHelper.add_user(new_user)
        response = self.testHelper.get_user_by_id(user_id=1)
        result = json.loads(response.data.decode())
        self.assertEqual(result["user"]['first_name'], new_user['first_name'])

    def test_change_user_role(self):
        """Test API promotes user to admin (PUT request)"""

        response = self.testHelper.change_user_role(user_id=1)
        result = json.loads(response.data.decode())
        self.assertEqual(result["message"], "User not found")

    def test_delete_user(self):
        """Test API delete user (DELETE request)"""

        response = self.testHelper.delete_user(user_id=1)
        result = json.loads(response.data.decode())
        self.assertEqual(result["message"], "User not found")

    def test_update_profile(self):
        """Test API update user profile (PUT request)"""

        response = self.testHelper.update_profile(user_id=1)
        result = json.loads(response.data.decode())
        self.assertEqual(result["message"], "User not found")

   