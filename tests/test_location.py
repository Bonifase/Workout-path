import unittest
import json
from tests import BaseTestSetUp
from tests.data import *


class TestUserCase(BaseTestSetUp):

    def test_get_all_locations(self):
        """Test API get all locations (GET request)"""

        response = self.testHelper.get_locations()
        result = json.loads(response.data.decode())
        self.assertEqual(result["message"], "No locations")

    def test_new_location_works(self):
        """Test API creates new location successfully (POST request)"""

        response = self.testHelper.add_location(new_location)
        result = json.loads(response.data.decode())
        self.assertEqual(result[
            "message"], new_location['name'] + " created")
        self.assertEqual(response.status_code, 201)
    
    def test_get_user_by_id(self):
        """Test API get one location (GET request)"""

        response = self.testHelper.get_location(location_id=1)
        result = json.loads(response.data.decode())
        self.assertEqual(result["message"], "Location not found")
