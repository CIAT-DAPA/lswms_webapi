import unittest
from unittest.mock import patch, MagicMock
from flask import Flask
from flask_restful import Api
from datetime import datetime
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from api_modules.mean import GetMean

class TestGetMean(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.api = Api(self.app)
        self.api.add_resource(GetMean, '/api/v1/mean')
        self.client = self.app.test_client()

    @patch('api_modules.mean.Woreda')
    @patch('api_modules.mean.Trend')
    def test_get_mean_success(self, MockTrend, MockWoreda):
        # Mock Woreda query result
        mock_woreda = MagicMock(id="1", ext_id="ET050788")
        MockWoreda.objects.return_value.first.return_value = mock_woreda

        # Mock Trend query result
        mock_trend = MagicMock(mean=1.23)
        MockTrend.objects.return_value.only.return_value.first.return_value = mock_trend

        # Make a GET request to the endpoint
        response = self.client.get('/api/v1/mean?extId=ET050788&timestamp=2022-01-01')

        # Assert the response status code and data
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"meanBiomass": 1.23})

    @patch('api_modules.mean.Woreda') 
    def test_get_mean_woreda_not_found(self, MockWoreda):
        # Mock Woreda query result to return None
        MockWoreda.objects.return_value.first.return_value = None

        # Make a GET request to the endpoint
        response = self.client.get('/api/v1/mean?extId=ET999999&timestamp=2022-01-01')

        # Assert the response status code and data
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {"error": "Woreda not found."})

    @patch('api_modules.mean.Woreda')
    @patch('api_modules.mean.Trend')
    def test_get_mean_no_biomass_data(self, MockTrend, MockWoreda):
        # Mock Woreda query result
        mock_woreda = MagicMock(id="1", ext_id="ET050788")
        MockWoreda.objects.return_value.first.return_value = mock_woreda

        # Mock Trend query result to return None
        MockTrend.objects.return_value.only.return_value.first.return_value = None

        # Make a GET request to the endpoint
        response = self.client.get('/api/v1/mean?extId=ET050788&timestamp=2022-01-01')

        # Assert the response status code and data
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"meanBiomass": None})

    def test_get_mean_missing_parameters(self):
        # Make a GET request without parameters
        response = self.client.get('/api/v1/mean')

        # Assert the response status code and data
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json, {"error": "extId and timestamp are required."})

    def test_get_mean_invalid_date_format(self):
        # Make a GET request with invalid date format
        response = self.client.get('/api/v1/mean?extId=ET050788&timestamp=01-01-2022')

        # Assert the response status code and data
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json, {"error": "Invalid date format. Expected YYYY-MM-DD."})

if __name__ == '__main__':
    unittest.main()
