import mock
import json
import unittest

from plantpredict.prediction import Prediction
from tests import plantpredict_unit_test_case, mocked_requests


class TestPrediction(plantpredict_unit_test_case.PlantPredictUnitTestCase):
    @mock.patch('plantpredict.plant_predict_entity.PlantPredictEntity.create')
    def test_create(self, mocked_create):
        self._make_mocked_api()
        prediction = Prediction(api=self.mocked_api, project_id=7)

        prediction.create(use_closest_ashrae_station=False)
        self.assertEqual(prediction.create_url_suffix, "/Project/7/Prediction")
        self.assertTrue(mocked_create.called)

    @mock.patch('plantpredict.ashrae.requests.get', new=mocked_requests.mocked_requests_get)
    @mock.patch('plantpredict.project.requests.get', new=mocked_requests.mocked_requests_get)
    def test_assign_plant_design_temperature_with_closest_ashrae_station(self):
        self._make_mocked_api()
        prediction = Prediction(api=self.mocked_api, project_id=7)

        prediction._assign_plant_design_temperature_with_closest_ashrae_station()
        self.assertEqual(prediction.ashrae_station, "TEST STATION")
        self.assertEqual(prediction.cool_996, 20.0)
        self.assertEqual(prediction.max_50_year, 17.0)
        self.assertEqual(prediction.min_50_year, -20.0)

    @mock.patch('plantpredict.plant_predict_entity.PlantPredictEntity.delete')
    def test_delete(self, mocked_delete):
        self._make_mocked_api()
        prediction = Prediction(api=self.mocked_api, id=77, project_id=7)

        prediction.delete()
        self.assertEqual(prediction.delete_url_suffix, "/Project/7/Prediction/77")
        self.assertTrue(mocked_delete.called)

    @mock.patch('plantpredict.plant_predict_entity.PlantPredictEntity.get')
    def test_get(self, mocked_get):
        self._make_mocked_api()
        prediction = Prediction(api=self.mocked_api, id=77, project_id=7)

        prediction.get()
        self.assertEqual(prediction.get_url_suffix, "/Project/7/Prediction/77")
        self.assertTrue(mocked_get.called)

    @mock.patch('plantpredict.plant_predict_entity.PlantPredictEntity.update')
    def test_update(self, mocked_update):
        self._make_mocked_api()
        prediction = Prediction(api=self.mocked_api, project_id=7)

        prediction.update()
        self.assertEqual(prediction.update_url_suffix, "/Project/7/Prediction")
        self.assertTrue(mocked_update.called)

    @mock.patch('plantpredict.prediction.Prediction._wait_for_prediction')
    @mock.patch('plantpredict.prediction.requests.post', new=mocked_requests.mocked_requests_post)
    def test_run(self, mocked_wait_for_prediction):
        self._make_mocked_api()
        prediction = Prediction(api=self.mocked_api, project_id=710, id=555)

        is_success = prediction.run()
        self.assertTrue(mocked_wait_for_prediction.called)
        self.assertEqual(is_success["is_successful"], True)

    @mock.patch('plantpredict.prediction.requests.get', new=mocked_requests.mocked_requests_get)
    def test_get_results_summary(self):
        self._make_mocked_api()
        prediction = Prediction(api=self.mocked_api, project_id=710, id=555)

        response = prediction.get_results_summary()
        self.assertEqual(json.loads(response.content), {
            "prediction_name": "Test Prediction", "block_result_summaries": [{"name": 1}]
        })

    @mock.patch('plantpredict.prediction.requests.get', new=mocked_requests.mocked_requests_get)
    def test_get_results_details(self):
        self._make_mocked_api()
        prediction = Prediction(api=self.mocked_api, project_id=710, id=555)

        response = prediction.get_results_details()
        self.assertEqual(json.loads(response.content), {"prediction_name": "Test Prediction Details"})

    @mock.patch('plantpredict.prediction.requests.get', new=mocked_requests.mocked_requests_get)
    def test_get_nodal_data(self):
        self._make_mocked_api()
        prediction = Prediction(api=self.mocked_api, project_id=710, id=555)

        nodal_data_dc_field = prediction.get_nodal_data(params={
            'block_number': 1,
            'array_number': 1,
            'inverter_name': 'A',
            'dc_field_number': 1
        })
        self.assertEqual(nodal_data_dc_field, {"nodal_data_dc_field": {}})

    @mock.patch('plantpredict.prediction.requests.post', new=mocked_requests.mocked_requests_post)
    @mock.patch('plantpredict.prediction.requests.get', new=mocked_requests.mocked_requests_get)
    def test_clone(self):
        self._make_mocked_api()

        prediction = Prediction(api=self.mocked_api, id=555, project_id=710)
        prediction.created_date = '2019-06-28 11:26:00'
        prediction.last_modified = '2019-06-28 11:26:00'
        prediction.last_modified_by = 'Stephen Kaplan'
        prediction.last_modified_by_id = 1
        prediction.project = {"id": 710}
        prediction.powerplant_id = 10101
        prediction.powerplant_id = {"powerplant_id": 10101}

        new_prediction_id = prediction.clone(new_prediction_name="Cloned Prediction")
        self.assertEqual(new_prediction_id, 556)

    def test_init_minimum_inputs(self):
        self._make_mocked_api()
        prediction = Prediction(api=self.mocked_api)

        self.assertEqual(prediction.api, self.mocked_api)
        with self.assertRaises(AttributeError):
            print(prediction.id)
        self.assertIsNone(prediction.project_id)
        self.assertIsNone(prediction.name)

        self.assertIsNone(prediction.status)
        self.assertIsNone(prediction.year_repeater)
        self.assertIsNone(prediction.error_spa_var)
        self.assertIsNone(prediction.error_model_acc)
        self.assertIsNone(prediction.error_int_ann_var)
        self.assertIsNone(prediction.error_sens_acc)
        self.assertIsNone(prediction.error_mon_acc)

    def test_init_maximum_inputs(self):
        self._make_mocked_api()
        prediction = Prediction(api=self.mocked_api, id=77, project_id=7, name="Test Prediction")
        self.assertEqual(prediction.api, self.mocked_api)
        self.assertEqual(prediction.id, 77)
        self.assertEqual(prediction.project_id, 7)
        self.assertEqual(prediction.name, "Test Prediction")

        self.assertIsNone(prediction.status)
        self.assertIsNone(prediction.year_repeater)
        self.assertIsNone(prediction.error_spa_var)
        self.assertIsNone(prediction.error_model_acc)
        self.assertIsNone(prediction.error_int_ann_var)
        self.assertIsNone(prediction.error_sens_acc)
        self.assertIsNone(prediction.error_mon_acc)


if __name__ == '__main__':
    unittest.main()
