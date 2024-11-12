import unittest
from unittest.mock import patch, MagicMock
from flask import Flask
from flask_restful import Api
from datetime import datetime
from api_modules.forecast import GetForecast

class TestGetForecast(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.api = Api(self.app)
        self.api.add_resource(GetForecast, '/api/v1/forecast')
        self.client = self.app.test_client()

    @patch('api_modules.forecast.Woreda')
    @patch('api_modules.forecast.Trend')
    @patch('api_modules.forecast.Forecast')
    def test_get_forecast_success(self, MockForecast, MockTrend, MockWoreda):
        # Mock Woreda
        mock_woreda = MagicMock(id="1", ext_id="ET050788")
        MockWoreda.objects.return_value.first.return_value = mock_woreda

        # Mock Trend
        mock_trend = MagicMock(date=datetime(2022, 1, 1), mean=1.23)
        MockTrend.objects.return_value.order_by.return_value.only.return_value.first.return_value = mock_trend

        # Mock Forecast
        mock_forecast = [
            MagicMock(date=datetime(2022, 2, 1), mean=1.45),
            MagicMock(date=datetime(2022, 3, 1), mean=1.67),
        ]
        MockForecast.objects.return_value.order_by.return_value.only.return_value.limit.return_value = mock_forecast

        # Test the endpoint
        response = self.client.get('/api/v1/forecast?extId=ET050788')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json,
            [
                {"date": "2022-01-01", "mean": 1.23},
                {"date": "2022-02-01", "mean": 1.45},
                {"date": "2022-03-01", "mean": 1.67},
            ],
        )

    @patch('api_modules.forecast.Woreda')
    @patch('api_modules.forecast.Trend')
    @patch('api_modules.forecast.Forecast')
    def test_get_forecast_no_forecast_data(self, MockForecast, MockTrend, MockWoreda):
        # Mock Woreda
        mock_woreda = MagicMock(id="1", ext_id="ET050788")
        MockWoreda.objects.return_value.first.return_value = mock_woreda

        # Mock Trend
        mock_trend = MagicMock(date=datetime(2022, 1, 1), mean=1.23)
        MockTrend.objects.return_value.order_by.return_value.only.return_value.first.return_value = mock_trend

        # Mock Forecast to return empty list
        MockForecast.objects.return_value.order_by.return_value.only.return_value.limit.return_value = []

        # Test the endpoint
        response = self.client.get('/api/v1/forecast?extId=ET050788')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json,
            [
                {"date": "2022-01-01", "mean": 1.23},
            ],
        )

    @patch('api_modules.forecast.Woreda')
    def test_get_forecast_woreda_not_found(self, MockWoreda):
        # Mock Woreda to return None
        MockWoreda.objects.return_value.first.return_value = None

        # Test the endpoint
        response = self.client.get('/api/v1/forecast?extId=INVALID_ID')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {"error": "Woreda not found."})

    def test_get_forecast_missing_extId(self):
        # Test the endpoint without extId
        response = self.client.get('/api/v1/forecast')
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json, {"error": "extId is required."})

if __name__ == '__main__':
    unittest.main()
