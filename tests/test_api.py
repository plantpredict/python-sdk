import unittest
import mock

import plantpredict
from plantpredict import project, prediction, powerplant, geo, inverter, module, weather, ashrae
from tests import mocked_requests


class TestApi(unittest.TestCase):
    @mock.patch('plantpredict.api.requests.post', new=mocked_requests.mocked_requests_post)
    def setUp(self):
        self.api = plantpredict.Api(
            username="dummy username",
            password="dummy password",
            client_id="dummy client id",
            client_secret="dummy client secret"
        )

    @mock.patch('plantpredict.api.requests.post', new=mocked_requests.mocked_requests_post)
    def test_refresh_access_token(self):
        self.api.refresh_access_token()

        self.assertEqual(self.api.access_token, "dummy access token 2")
        self.assertEqual(self.api.refresh_token, "dummy refresh token 2")

    def test_init(self):
        self.assertEqual(self.api.base_url, "https://api.plantpredict.com")
        self.assertEqual(self.api.username, "dummy username")
        self.assertEqual(self.api.password, "dummy password")
        self.assertEqual(self.api.client_id, "dummy client id")
        self.assertEqual(self.api.client_secret, "dummy client secret")
        self.assertEqual(self.api.access_token, "dummy access token")
        self.assertEqual(self.api.refresh_token, "dummy refresh token")

    def test_project(self):
        self.assertIsInstance(self.api.project(), project.Project)

    def test_prediction(self):
        self.assertIsInstance(self.api.prediction(), prediction.Prediction)

    def test_powerplant(self):
        self.assertIsInstance(self.api.powerplant(), powerplant.PowerPlant)

    def test_geo(self):
        self.assertIsInstance(self.api.geo(), geo.Geo)

    def test_inverter(self):
        self.assertIsInstance(self.api.inverter(), inverter.Inverter)

    def test_module(self):
        self.assertIsInstance(self.api.module(), module.Module)

    def test_weather(self):
        self.assertIsInstance(self.api.weather(), weather.Weather)

    def test_ashrae(self):
        self.assertIsInstance(self.api.ashrae(), ashrae.ASHRAE)


if __name__ == '__main__':
    unittest.main()
