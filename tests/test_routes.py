
import unittest
from unittest.mock import patch

from app import create_app
from app.database import get_connection


class TestEcoPulse(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.app.config["TESTING"] = True
        cls.client = cls.app.test_client()

    def test_dashboard(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    @patch("app.routes.obter_clima_atual")
    @patch("app.routes.obter_qualidade_ar")
    def test_weather(self, mock_air, mock_weather):
        mock_weather.return_value = {
            "location": "São Paulo - SP",
            "temperature": 25.0,
            "humidity": 60.0,
            "measured_at": "2026-11-16T15:00"
        }
        mock_air.return_value = {
            "air_quality": 40.0
        }

        response = self.client.get("/weather")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["temperature"], 25.0)
        self.assertEqual(response.json["humidity"], 60.0)
        self.assertEqual(response.json["air_quality"], 40.0)

    def test_history(self):
        response = self.client.get("/weather/history")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)

    def test_invalid_measurement(self):
        response = self.client.post(
            "/measurements",
            json={
                "temperature": 25,
                "humidity": 150,
                "air_quality": 40,
                "location": "São Paulo - SP"
            }
        )

        self.assertEqual(response.status_code, 400)

    def test_database_connection(self):
        connection = get_connection()

        try:
            result = connection.execute(
                "SELECT name FROM sqlite_master "
                "WHERE type='table' AND name='weather_measurements'"
            ).fetchone()

            self.assertIsNotNone(result)
        finally:
            connection.close()


if __name__ == "__main__":
    unittest.main()
