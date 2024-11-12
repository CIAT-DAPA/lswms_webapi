import unittest
from unittest.mock import patch, MagicMock
from flask import Flask
from flask_restful import Api
from datetime import datetime
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from api_modules.trend import GetTrend

class TestGetTrend(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.api = Api(self.app)
        self.api.add_resource(GetTrend, '/api/v1/trend')
        self.client = self.app.test_client()

    @patch('api_modules.trend.Woreda')
    @patch('api_modules.trend.Trend') 
    def test_get_trend_success(self, MockTrend, MockWoreda):
        # Mock Woreda query result
        mock_woreda = MagicMock(id="1", ext_id="ET050788")
        MockWoreda.objects.return_value.first.return_value = mock_woreda

        # Mock Trend query result
        mock_trends = [
            MagicMock(date=datetime(2022, 1, 1), mean=1.23),
            MagicMock(date=datetime(2022, 2, 1), mean=1.45),
        ]
        MockTrend.objects.return_value.order_by.return_value.only.return_value = mock_trends

        
        for trend in mock_trends:
            trend.date = trend.date.strftime('%Y-%m-%d')

        # Make a GET request to the endpoint
        response = self.client.get('/api/v1/trend?extId=ET050788')

        # Assert the response status code and data
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [
            {"date": "2022-01-01", "mean": 1.23},
            {"date": "2022-02-01", "mean": 1.45}
        ])

    @patch('api_modules.trend.Woreda')  
    @patch('api_modules.trend.Trend') 
    def test_get_trend_no_trend_data(self, MockTrend, MockWoreda):
        # Mock Woreda query result
        mock_woreda = MagicMock(id="1", ext_id="ET050788")
        MockWoreda.objects.return_value.first.return_value = mock_woreda

        # Mock Trend query result to return no data
        MockTrend.objects.return_value.order_by.return_value.only.return_value = []

        # Make a GET request to the endpoint
        response = self.client.get('/api/v1/trend?extId=ET050788')

        # Assert the response status code and data
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, []) 

    @patch('api_modules.trend.Woreda')  
    def test_get_trend_woreda_not_found(self, MockWoreda):
        # Mock Woreda query result to return None
        MockWoreda.objects.return_value.first.return_value = None

        # Make a GET request to the endpoint
        response = self.client.get('/api/v1/trend?extId=ET999999')

        # Assert the response status code and data
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {"error": "Woreda not found."})

    def test_get_trend_missing_extId(self):
        # Make a GET request without the extId parameter
        response = self.client.get('/api/v1/trend')

        # Assert the response status code and data
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json, {"error": "extId is required."})

if __name__ == '__main__':
    unittest.main()
