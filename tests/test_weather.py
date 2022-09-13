import mock
import json
import unittest

from plantpredict.weather import Weather
from tests import plantpredict_unit_test_case, mocked_requests
from plantpredict.enumerations import WeatherSourceTypeAPIEnum


class TestWeather(plantpredict_unit_test_case.PlantPredictUnitTestCase):
    @mock.patch('plantpredict.plant_predict_entity.PlantPredictEntity.create')
    def test_create(self, mocked_create):
        self._make_mocked_api()
        weather = Weather(api=self.mocked_api)

        weather.create()
        self.assertEqual(weather.create_url_suffix, "/Weather")
        self.assertTrue(mocked_create.called)

    @mock.patch('plantpredict.plant_predict_entity.PlantPredictEntity.delete')
    def test_delete(self, mocked_delete):
        self._make_mocked_api()
        weather = Weather(api=self.mocked_api, id=999)

        weather.delete()
        self.assertEqual(weather.delete_url_suffix, "/Weather/999")
        self.assertTrue(mocked_delete.called)

    @mock.patch('plantpredict.plant_predict_entity.PlantPredictEntity.get')
    def test_get(self, mocked_get):
        self._make_mocked_api()
        weather = Weather(api=self.mocked_api, id=999)

        weather.get()
        self.assertEqual(weather.get_url_suffix, "/Weather/999")
        self.assertTrue(mocked_get.called)

    @mock.patch('plantpredict.plant_predict_entity.PlantPredictEntity.update')
    def test_update(self, mocked_update):
        self._make_mocked_api()
        weather = Weather(api=self.mocked_api, id=999)

        weather.update()
        self.assertEqual(weather.update_url_suffix, "/Weather")
        self.assertTrue(mocked_update.called)

    @mock.patch('plantpredict.weather.requests.get', new=mocked_requests.mocked_requests_get)
    def test_get_details(self):
        self._make_mocked_api()
        weather = Weather(api=self.mocked_api, id=999)

        response = weather.get_details()
        self.assertEqual(response.json(), {"id": 999, "name": "Weather File"})

    @mock.patch('plantpredict.weather.requests.get', new=mocked_requests.mocked_requests_get)
    def test_search(self):
        self._make_mocked_api()
        weather = Weather(api=self.mocked_api)

        search_results = weather.search(latitude=39.67, longitude=-105.21)
        self.assertEqual(search_results, [{"id": 998, "name": "Weather File 2"}])

    @mock.patch('plantpredict.weather.requests.post', new=mocked_requests.mocked_requests_post)
    def test_download(self):
        self._make_mocked_api()
        weather = Weather(api=self.mocked_api)

        response = weather.download(latitude=39.67, longitude=-105.21, provider=WeatherSourceTypeAPIEnum.METEONORM)
        self.assertEqual(response.json(), {"id": 997, "name": "Downloaded Weather File"})
        self.assertEqual(weather.id, 997)


if __name__ == '__main__':
    unittest.main()
