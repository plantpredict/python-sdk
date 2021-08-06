import mock
import json
import unittest

from plantpredict.ashrae import ASHRAE
from tests import plantpredict_unit_test_case, mocked_requests


class TestPrediction(plantpredict_unit_test_case.PlantPredictUnitTestCase):
    @mock.patch('plantpredict.ashrae.requests.get', new=mocked_requests.mocked_requests_get)
    def test_get_station(self):
        self._make_mocked_api()
        ashrae = ASHRAE(api=self.mocked_api, latitude=35.0, longitude=-109.0)
        response = ashrae.get_station(station_name="TEST STATION")

        self.assertEqual(json.loads(response.content), {
                "station_name": "TEST STATION",
                "wmo": 18081,
                "cool_996": 20.0,
                "min_50_year": -20.0,
                "max_50_year": 17.0,
                "distance": 5.3,
                "latitude": 35.0,
                "longitude": -109.0
        })
        self.assertEqual(ashrae.cool_996, 20.0)

    @mock.patch('plantpredict.ashrae.requests.get', new=mocked_requests.mocked_requests_get)
    def test_get_closest_station(self):
        self._make_mocked_api()
        ashrae = ASHRAE(api=self.mocked_api, latitude=33.0, longitude=-110.0)
        response = ashrae.get_closest_station()

        self.assertEqual(json.loads(response.content), {
                "station_name": "TEST STATION",
                "wmo": 18081,
                "cool_996": 20.0,
                "min_50_year": -20.0,
                "max_50_year": 17.0,
                "distance": 5.3,
                "latitude": 35.0,
                "longitude": -109.0
        })
        self.assertEqual(ashrae.cool_996, 20.0)

