import mock
import json
import unittest

from plantpredict.project import Project
from tests import plantpredict_unit_test_case, mocked_requests


class TestProject(plantpredict_unit_test_case.PlantPredictUnitTestCase):
    @mock.patch('plantpredict.plant_predict_entity.PlantPredictEntity.create')
    def test_create(self, mocked_create):
        self._make_mocked_api()
        project = Project(api=self.mocked_api)

        project.create()
        self.assertEqual(project.create_url_suffix, "/Project")
        self.assertTrue(mocked_create.called)

    @mock.patch('plantpredict.plant_predict_entity.PlantPredictEntity.delete')
    def test_delete(self, mocked_delete):
        self._make_mocked_api()
        project = Project(api=self.mocked_api, id=710)

        project.delete()
        self.assertEqual(project.delete_url_suffix, "/Project/710")
        self.assertTrue(mocked_delete.called)

    @mock.patch('plantpredict.plant_predict_entity.PlantPredictEntity.get')
    def test_get(self, mocked_get):
        self._make_mocked_api()
        project = Project(api=self.mocked_api, id=710)

        project.get()
        self.assertEqual(project.get_url_suffix, "/Project/710")
        self.assertTrue(mocked_get.called)

    @mock.patch('plantpredict.plant_predict_entity.PlantPredictEntity.update')
    def test_update(self, mocked_update):
        self._make_mocked_api()
        project = Project(api=self.mocked_api, id=710)

        project.update()
        self.assertEqual(project.update_url_suffix, "/Project")
        self.assertTrue(mocked_update.called)

    @mock.patch('plantpredict.project.requests.get', new=mocked_requests.mocked_requests_get)
    def test_get_all_predictions(self):
        self._make_mocked_api()
        project = Project(api=self.mocked_api, id=710)

        response = project.get_all_predictions()
        self.assertEqual(json.loads(response.content), [
            {"project_id": 1, "name": "Project 1"},
            {"project_id": 2, "name": "Project 2"},
            {"project_id": 3, "name": "Project 3"}
        ])

    @mock.patch('plantpredict.project.requests.get', new=mocked_requests.mocked_requests_get)
    def test_search(self):
        self._make_mocked_api()
        project = Project(api=self.mocked_api)

        response = project.search(latitude=33.0, longitude=-118.0, search_radius=2)
        self.assertEqual(response, [{"project_id": 1, "name": "Project 1"}])

    def test_assign_location_attributes(self):
        self._make_mocked_api()
        project = Project(api=self.mocked_api, latitude=39.67, longitude=-105.21, name="Test Project")

        project.assign_location_attributes()
        self.assertEqual(project.country, "United States")
        self.assertEqual(project.country_code, "US")
        self.assertEqual(project.locality, "Morrison")
        self.assertEqual(project.region, "North America")
        self.assertEqual(project.state_province, "Colorado")
        self.assertEqual(project.state_province_code, "CO")

    def test_init_without_id(self):
        self._make_mocked_api()
        project = Project(api=self.mocked_api, latitude=39.67, longitude=-105.21, name="Test Project")

        with self.assertRaises(AttributeError):
            print(project.id)
        self.assertEqual(project.api, self.mocked_api)
        self.assertEqual(project.latitude, 39.67)
        self.assertEqual(project.longitude, -105.21)
        self.assertEqual(project.name, "Test Project")
        self.assertIsNone(project.locality)
        self.assertIsNone(project.state_province_code)
        self.assertIsNone(project.state_province)
        self.assertIsNone(project.country_code)
        self.assertIsNone(project.country)
        self.assertIsNone(project.region)
        self.assertIsNone(project.elevation)
        self.assertIsNone(project.standard_offset_from_utc)

    def test_init_with_id(self):
        self._make_mocked_api()
        project = Project(api=self.mocked_api, latitude=39.67, longitude=-105.21, name="Test Project", id=101)

        self.assertEqual(project.id, 101)
        self.assertEqual(project.api, self.mocked_api)
        self.assertEqual(project.latitude, 39.67)
        self.assertEqual(project.longitude, -105.21)
        self.assertEqual(project.name, "Test Project")
        self.assertIsNone(project.locality)
        self.assertIsNone(project.state_province_code)
        self.assertIsNone(project.state_province)
        self.assertIsNone(project.country_code)
        self.assertIsNone(project.country)
        self.assertIsNone(project.region)
        self.assertIsNone(project.elevation)
        self.assertIsNone(project.standard_offset_from_utc)


if __name__ == '__main__':
    unittest.main()
