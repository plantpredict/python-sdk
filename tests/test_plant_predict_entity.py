import unittest
import mock
import json

from plantpredict.plant_predict_entity import PlantPredictEntity
from tests import plantpredict_unit_test_case, mocked_requests
from plantpredict.error_handlers import APIError


class TestPlantPredictEntity(plantpredict_unit_test_case.PlantPredictUnitTestCase):

    @mock.patch('plantpredict.plant_predict_entity.requests.post', mocked_requests.mocked_requests_post)
    def test_create(self):
        self._make_mocked_api()
        ppe = PlantPredictEntity(self.mocked_api)
        ppe.create_url_suffix = "/create-info/80206"

        response = ppe.create()
        self.assertEqual(json.loads(response.content), {"id": 35})
        self.assertEqual(ppe.id, 35)

    @mock.patch('plantpredict.plant_predict_entity.requests.delete', mocked_requests.mocked_requests_delete)
    def test_delete(self):
        self._make_mocked_api()
        ppe = PlantPredictEntity(self.mocked_api)
        ppe.delete_url_suffix = "/delete-info/80206"

        response = ppe.delete()
        self.assertEqual(json.loads(response.content), {"success": True})

    @mock.patch('plantpredict.plant_predict_entity.requests.get', mocked_requests.mocked_requests_get)
    def test_get_success(self):
        self._make_mocked_api()
        ppe = PlantPredictEntity(self.mocked_api)
        ppe.get_url_suffix = "/get-info/80206"

        response = ppe.get()
        self.assertEqual(json.loads(response.content), {"color": "blue"})
        self.assertEqual(ppe.color, "blue")

    @mock.patch('plantpredict.plant_predict_entity.requests.get', mocked_requests.mocked_requests_get)
    def test_get_no_entity_found(self):
        self._make_mocked_api()
        ppe = PlantPredictEntity(self.mocked_api)
        ppe.get_url_suffix = "/get-info/80207"

        with self.assertRaises(APIError) as e:
            response = ppe.get()

        self.assertEqual(e.exception.args[0], 404)
        self.assertEqual(e.exception.args[1], "Info not found.")

    @mock.patch('plantpredict.plant_predict_entity.requests.put', mocked_requests.mocked_requests_update)
    def test_update(self):
        self._make_mocked_api()
        ppe = PlantPredictEntity(self.mocked_api)
        ppe.update_url_suffix = "/update-info/80206"

        response = ppe.update()
        self.assertEqual(json.loads(response.content), {"color": "red"})

    def test_init(self):
        self._make_mocked_api()
        ppe = PlantPredictEntity(self.mocked_api)

        self.assertEqual(ppe.api, self.mocked_api)
        self.assertEqual(ppe.create_url_suffix, None)
        self.assertEqual(ppe.get_url_suffix, None)
        self.assertEqual(ppe.update_url_suffix, None)
        self.assertEqual(ppe.delete_url_suffix, None)


if __name__ == '__main__':
    unittest.main()
