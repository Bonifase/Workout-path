import unittest
import json
from tests import BaseTestSetUp
from tests.data import *


class TestUserCase(BaseTestSetUp):

    def test_get_all_locations(self):
        """Test API get all users (GET request)"""

        response = self.testHelper.get_locations()
        result = json.loads(response.data.decode())
        self.assertEqual(result["message"], "No locations")
