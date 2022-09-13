import unittest
import mock
import json

import plantpredict
from plantpredict.geo import Geo
from tests import plantpredict_unit_test_case, mocked_requests


class TestGeo(plantpredict_unit_test_case.PlantPredictUnitTestCase):
    @mock.patch('plantpredict.geo.requests.get', new=mocked_requests.mocked_requests_get)
    def test_get_location_info(self):
        self._make_mocked_api()
        geo = Geo(api=self.mocked_api, latitude=39.67, longitude=-105.21)
        response = geo.get_location_info()

        self.assertEqual(response.json(), {
            "country": "United States",
            "country_code": "US",
            "locality": "Morrison",
            "region": "North America",
            "state_province": "Colorado",
            "state_province_code": "CO"
        })
        self.assertEqual(geo.country, "United States")
        self.assertEqual(geo.country_code, "US")
        self.assertEqual(geo.locality, "Morrison")
        self.assertEqual(geo.region, "North America")
        self.assertEqual(geo.state_province, "Colorado")
        self.assertEqual(geo.state_province_code, "CO")

    @mock.patch('plantpredict.geo.requests.get', new=mocked_requests.mocked_requests_get)
    def test_get_elevation(self):
        self._make_mocked_api()
        geo = Geo(api=self.mocked_api, latitude=39.67, longitude=-105.21)
        response = geo.get_elevation()

        self.assertEqual(response.json(), {"elevation": 1965.96})
        self.assertEqual(geo.elevation, 1965.96)

    @mock.patch('plantpredict.geo.requests.get', new=mocked_requests.mocked_requests_get)
    def test_get_time_zone(self):
        self._make_mocked_api()
        geo = Geo(api=self.mocked_api, latitude=39.67, longitude=-105.21)
        response = geo.get_time_zone()

        self.assertEqual(response.json(), {"time_zone": -7.0})

    @mock.patch('plantpredict.api.requests.post', autospec=True)
    def test_init(self, mock_api_post):
        mock_api_post.return_value.ok = True
        mock_api_post.return_value.content = '''{"access_token":"dummy_access_token",
                                            "refresh_token":"dummy_refresh_token"}'''
        api = plantpredict.Api(client_id="0oakq", client_secret="IEdpr")

        geo = Geo(api=api, latitude=39.67, longitude=-105.21)
        self.assertIsInstance(geo, Geo)
        self.assertIsInstance(geo.api, plantpredict.Api)
        self.assertEqual(geo.latitude, 39.67)
        self.assertEqual(geo.longitude, -105.21)


if __name__ == '__main__':
    unittest.main()
