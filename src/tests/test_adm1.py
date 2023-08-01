import unittest
import sys,os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from wpapi import app

from mongoengine import connect, disconnect

class TestAdm1(unittest.TestCase):

    def setUp(self):
        connect('mongoenginetest', host='mongomock://localhost')
        self.app = app.test_client()

    def tearDown(self):
        disconnect()

    def test_single_adm1_valid_id(self):
        # Test a valid adm1 ID
        response = self.app.get('http://127.0.0.1:5000/api/v1/adm1', headers={"Content-Type": "application/json"})
        self.assertEqual(200, response.status_code)
        # Add more assertions to check the response content

    def test_single_adm1_invalid_id(self):
        # Test an invalid adm1 ID
        response = self.app.get('http://127.0.0.1:5000/adm1/invalid_id', headers={"Content-Type": "application/json"})
        self.assertEqual(404, response.status_code)
        # Add more assertions to check the response content

    def test_single_adm1_no_id(self):
        # Test the endpoint without providing an ADM1 ID
        response = self.app.get('http://127.0.0.1:5000/adm1/', headers={"Content-Type": "application/json"})
        self.assertEqual(404, response.status_code)

    def test_single_adm1_wrong_method(self):
        # Test using an unsupported HTTP method for the endpoint
        response = self.app.post('http://127.0.0.1:5000/adm1/637e450d6b22dee825f5b35b', headers={"Content-Type": "application/json"})
        self.assertEqual(404, response.status_code)

    # Add more test cases to cover other scenarios if needed

if __name__ == "__main__":
    unittest.main()
