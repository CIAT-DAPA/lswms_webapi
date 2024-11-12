import unittest
from unittest.mock import patch, MagicMock
from flask import Flask
from flask_restful import Api
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from api_modules.forecast_update import ForecastUpdate

class TestForecastUpdate(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.api = Api(self.app)
        self.api.add_resource(ForecastUpdate, '/api/v1/forecasts')
        self.client = self.app.test_client()
        self.api_key = "Bearer prueba"

    @patch('api_modules.forecast_update.Woreda')
    @patch('api_modules.forecast_update.Forecast')
    def test_forecast_update_success(self, MockForecast, MockWoreda):
        mock_woreda = MagicMock(id="1")
        MockWoreda.objects.return_value.first.return_value = mock_woreda

        payload = [
            {"extId": "ET010101", "mean": 1.23, "date": "2022-01-01"}
        ]

        response = self.client.post(
            '/api/v1/forecasts',
            json=payload,
            headers={"Authorization": self.api_key}
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json, {"message": "All forecasts saved or updated successfully"})

    @patch('api_modules.forecast_update.Woreda')
    @patch('api_modules.forecast_update.Forecast')
    def test_forecast_update_woreda_not_found(self, MockForecast, MockWoreda):
        MockWoreda.objects.return_value.first.return_value = None

        payload = [
            {"extId": "ET010101", "mean": 1.23, "date": "2022-01-01"}
        ]

        response = self.client.post(
            '/api/v1/forecasts',
            json=payload,
            headers={"Authorization": self.api_key}
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {"error": "Woreda not found for extId ET010101"})

    @patch('api_modules.forecast_update.Woreda')
    @patch('api_modules.forecast_update.Forecast')
    def test_forecast_update_validation_error(self, MockForecast, MockWoreda):
        mock_woreda = MagicMock(id="1")
        MockWoreda.objects.return_value.first.return_value = mock_woreda

        payload = [{"extId": "ET010101", "mean": None, "date": None}]

        response = self.client.post(
            '/api/v1/forecasts',
            json=payload,
            headers={"Authorization": self.api_key}
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json)
        self.assertIn("Invalid data:", response.json["error"])
        self.assertIn("'extId': 'ET010101'", response.json["error"])
        self.assertIn("'mean': None", response.json["error"])
        self.assertIn("'date': None", response.json["error"])

    @patch('api_modules.forecast_update.Woreda')
    @patch('api_modules.forecast_update.Forecast')
    def test_forecast_update_server_error(self, MockForecast, MockWoreda):
        mock_woreda = MagicMock(id="1")
        MockWoreda.objects.return_value.first.return_value = mock_woreda
        MockForecast.objects.side_effect = Exception("Database connection failed")

        payload = [
            {"extId": "ET010101", "mean": 1.23, "date": "2022-01-01"}
        ]

        response = self.client.post(
            '/api/v1/forecasts',
            json=payload,
            headers={"Authorization": self.api_key}
        )

        self.assertEqual(response.status_code, 500)
        self.assertIn("error", response.json)
        self.assertIn("An error occurred:", response.json["error"])

    def test_forecast_update_missing_auth(self):
        payload = [
            {"extId": "ET010101", "mean": 1.23, "date": "2022-01-01"}
        ]

        response = self.client.post(
            '/api/v1/forecasts',
            json=payload
        )

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json, {"error": "Unauthorized"})

    def test_forecast_update_invalid_auth(self):
        payload = [
            {"extId": "ET010101", "mean": 1.23, "date": "2022-01-01"}
        ]

        response = self.client.post(
            '/api/v1/forecasts',
            json=payload,
            headers={"Authorization": "Bearer invalid_key"}
        )

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json, {"error": "Invalid API key"})


if __name__ == '__main__':
    unittest.main()
