import unittest
import mock

from plantpredict.prediction import Prediction
from plantpredict.module import Module
from plantpredict.project import Project
from plantpredict.ashrae import ASHRAE
from plantpredict.inverter import Inverter


class PlantPredictUnitTestCase(unittest.TestCase):
    def _mock_geo_with_all_methods_called(self):
        # created for mocking project.Project.get_location_attributes
        self.mocked_api.geo().country = "United States"
        self.mocked_api.geo().country_code = "US"
        self.mocked_api.geo().locality = "Morrison"
        self.mocked_api.geo().region = "North America"
        self.mocked_api.geo().state_province = "Colorado"
        self.mocked_api.geo().state_province_code = "CO"

    @mock.patch('plantpredict.api.Api')
    def _make_mocked_api(self, mocked_api, module_id=123):
        self.mocked_api = mocked_api()
        self.mocked_api.base_url = "https://api.plantpredict.com"
        self.mocked_api.access_token = 'dummy_token'

        self.mocked_api.prediction.return_value = Prediction(self.mocked_api)
        self.mocked_api.module.return_value = Module(api=self.mocked_api, id=module_id)
        self.mocked_api.project.return_value = Project(api=self.mocked_api, id=7)
        self.mocked_api.ashrae.return_value = ASHRAE(api=self.mocked_api, latitude=33.0, longitude=-110.0)

        self._mock_geo_with_all_methods_called()


