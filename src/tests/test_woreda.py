import sys
import os
import unittest
from unittest.mock import patch, MagicMock
from flask import Flask
from flask_restful import Api
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from api_modules.woreda import GetWoreda

class TestGetWoreda(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.api = Api(self.app)
        self.api.add_resource(GetWoreda, '/api/v1/woredas')
        self.client = self.app.test_client()

    @patch('api_modules.woreda.Woreda')
    def test_get_woredas_success(self, MockWoreda):
        
        mock_query_set = [
            MagicMock(id="1", name="Woreda 1", ext_id="ET010101"),
            MagicMock(id="2", name="Woreda 2", ext_id="ET010102"),
        ]
        
        mock_query_set[0].id = "1"
        mock_query_set[0].name = "Woreda 1"
        mock_query_set[0].ext_id = "ET010101"
        mock_query_set[1].id = "2"
        mock_query_set[1].name = "Woreda 2"
        mock_query_set[1].ext_id = "ET010102"

        MockWoreda.objects.return_value = mock_query_set

        # Make a GET request to the endpoint
        response = self.client.get('/api/v1/woredas')
        

        # Assert the response status code and data
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [
            {"id": "1", "name": "Woreda 1", "ext_id": "ET010101"},
            {"id": "2", "name": "Woreda 2", "ext_id": "ET010102"},
        ])

    @patch('api_modules.woreda.Woreda') 
    def test_get_woredas_server_error(self, MockWoreda):
        # Mock an exception in the database query
        MockWoreda.objects.side_effect = Exception("Database connection failed")

        # Make a GET request to the endpoint
        response = self.client.get('/api/v1/woredas')
        

        # Assert the response status code and error message
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {
            "error": "An error occurred while fetching the Woreda data.",
            "details": "Database connection failed",
        })

if __name__ == '__main__':
    unittest.main()
