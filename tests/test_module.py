import mock
import unittest
import json

from plantpredict.module import Module
from tests import plantpredict_unit_test_case, mocked_requests


class TestModule(plantpredict_unit_test_case.PlantPredictUnitTestCase):
    @mock.patch('plantpredict.plant_predict_entity.PlantPredictEntity.create')
    def test_create(self, mocked_create):
        self._make_mocked_api()
        module = Module(api=self.mocked_api)
        module.stc_short_circuit_current = 1.23
        module.stc_short_circuit_current_temp_coef = 0.04
        module.length = 2000
        module.width = 1200
        module.stc_max_power = 120.0

        module.create()
        self.assertEqual(module.create_url_suffix, "/Module")
        self.assertTrue(mocked_create.called)
        self.assertEqual(module.short_circuit_current_at_stc, 1.23)
        self.assertEqual(module.linear_temp_dependence_on_isc, 0.04)
        self.area = 2.4
        self.stc_efficiency = 120.0 / (2.4 * 1000.0)

    @mock.patch('plantpredict.plant_predict_entity.PlantPredictEntity.delete')
    def test_delete(self, mocked_delete):
        self._make_mocked_api()
        module = Module(api=self.mocked_api, id=808)

        module.delete()
        self.assertEqual(module.delete_url_suffix, "/Module/808")
        self.assertTrue(mocked_delete.called)

    @mock.patch('plantpredict.plant_predict_entity.PlantPredictEntity.get')
    def test_get(self, mocked_get):
        self._make_mocked_api()
        module = Module(api=self.mocked_api, id=808)

        module.get()
        self.assertEqual(module.get_url_suffix, "/Module/808")
        self.assertTrue(mocked_get.called)

    @mock.patch('plantpredict.plant_predict_entity.PlantPredictEntity.update')
    def test_update(self, mocked_update):
        self._make_mocked_api()
        module = Module(api=self.mocked_api, id=808)

        module.update()
        self.assertEqual(module.update_url_suffix, "/Module")
        self.assertTrue(mocked_update.called)

    def test_parse_full_iv_curves_template_no_sheet_name(self):
        self._make_mocked_api()
        module = Module(api=self.mocked_api)
        iv_curves = module._parse_full_iv_curves_template("test_data/test_parse_full_iv_curves_template.xlsx")

        self.assertEqual(len(iv_curves), 2)
        self.assertEqual(len(iv_curves[0]["data_points"]), 200)
        self.assertEqual(iv_curves[0]["temperature"], 25)
        self.assertEqual(len(iv_curves[1]["data_points"]), 200)
        self.assertEqual(iv_curves[1]["temperature"], 50)
        self.assertAlmostEqual(iv_curves[0]["data_points"][3]["current"], 2.450329288)
        self.assertAlmostEqual(iv_curves[1]["data_points"][198]["voltage"], 224.9763771)

    def test_parse_full_iv_curves_template_with_sheet_name(self):
        self._make_mocked_api()
        module = Module(api=self.mocked_api)
        iv_curves = module._parse_full_iv_curves_template(
            file_path="test_data/test_parse_full_iv_curves_template.xlsx",
            sheet_name="NewSheetName"
        )

        self.assertEqual(len(iv_curves), 1)
        self.assertEqual(len(iv_curves[0]["data_points"]), 200)
        self.assertEqual(iv_curves[0]["temperature"], 25)
        self.assertAlmostEqual(iv_curves[0]["data_points"][3]["current"], 2.450329288)

    def test_parse_key_iv_points_template_no_sheet_name(self):
        self._make_mocked_api()
        module = Module(api=self.mocked_api)
        key_iv_points = module._parse_key_iv_points_template(file_path="test_data/test_parse_key_iv_points_template.xlsx")

        self.assertEqual(len(key_iv_points), 27)
        self.assertEqual(key_iv_points[5]["temperature"], 15)
        self.assertEqual(key_iv_points[5]["irradiance"], 1000)
        self.assertEqual(key_iv_points[5]["short_circuit_current"], 1.74346881517)
        self.assertEqual(key_iv_points[5]["mpp_voltage"], 74.21342493)

    def test_parse_key_iv_points_template_with_sheet_name(self):
        self._make_mocked_api()
        module = Module(api=self.mocked_api)
        key_iv_points = module._parse_key_iv_points_template(
            file_path="test_data/test_parse_key_iv_points_template.xlsx",
            sheet_name="NewSheetName"
        )

        self.assertEqual(len(key_iv_points), 27)
        self.assertEqual(key_iv_points[5]["temperature"], 15)
        self.assertEqual(key_iv_points[5]["irradiance"], 1000)
        self.assertEqual(key_iv_points[5]["short_circuit_current"], 1.74346881517)
        self.assertEqual(key_iv_points[5]["mpp_voltage"], 74.21342493)

    @mock.patch('plantpredict.module.requests.post', new=mocked_requests.mocked_requests_post)
    def test_generate_iv_curve(self):
        self._make_mocked_api()
        module = Module(api=self.mocked_api)
        iv_curve = module.generate_iv_curve()
        module.num_iv_points = 100

        self.assertEqual(iv_curve, [{"current": 1.2, "voltage": 100.0}])

    def test_process_iv_curves_no_inputs(self):
        self._make_mocked_api()
        module = Module(api=self.mocked_api)

        with self.assertRaises(ValueError) as e:
            module.process_iv_curves()
        self.assertEqual(e.exception.args[0], "Either a file path to the .xslx template for Full IV Curves input or "
                                              "the properly formatted JSON-serializable data structure for Key IV "
                                              "Points input must be assigned as input. See the Python SDK "
                                              "documentation (https://plantpredict-python.readthedocs.io/en/latest/)"
                                              " for more information.")

    def test_process_iv_curves_conflicting_inputs(self):
        self._make_mocked_api()
        module = Module(api=self.mocked_api)

        with self.assertRaises(ValueError) as e:
            module.process_iv_curves(
                file_path="fake_file_path.xlsx",
                iv_curve_data={
                    "temperature": 25, "irradiance": 1000, "data_points": [{"current": 1.25, "voltage": 20.0}]
                }
            )
        self.assertEqual(e.exception.args[0], "Only one input option may be specified.")

    @mock.patch('plantpredict.module.requests.post', mocked_requests.mocked_requests_post)
    def test_process_iv_curves_with_file(self):
        self._make_mocked_api()
        module = Module(api=self.mocked_api)

        data = module.process_iv_curves(file_path="test_data/test_parse_full_iv_curves_template.xlsx")
        self.assertEqual(data, [
            {
                "temperature": 25,
                "irradiance": 1000,
                "short_circuit_current": 9.43,
                "open_circuit_voltage": 46.39,
                "mpp_current": 8.9598,
                "mpp_voltage": 38.1285,
                "max_power": 341.6237
            },
            {
                "temperature": 25,
                "irradiance": 1000,
                "short_circuit_current": 9.43,
                "open_circuit_voltage": 46.39,
                "mpp_current": 8.9598,
                "mpp_voltage": 38.1285,
                "max_power": 341.6237
            }
        ])

    @mock.patch('plantpredict.module.requests.post', mocked_requests.mocked_requests_post)
    def test_process_iv_curves_with_file(self):
        self._make_mocked_api()
        module = Module(api=self.mocked_api)

        data = module.process_iv_curves(iv_curve_data=[
            {"temperature": 25, "irradiance": 1000, "data_points": [{"current": 1.25, "voltage": 20.0}]},
            {"temperature": 25, "irradiance": 1000, "data_points": [{"current": 1.25, "voltage": 20.0}]}
        ])
        self.assertEqual(data, [
            {
                "temperature": 25,
                "irradiance": 1000,
                "short_circuit_current": 9.43,
                "open_circuit_voltage": 46.39,
                "mpp_current": 8.9598,
                "mpp_voltage": 38.1285,
                "max_power": 341.6237
            },
            {
                "temperature": 25,
                "irradiance": 1000,
                "short_circuit_current": 9.43,
                "open_circuit_voltage": 46.39,
                "mpp_current": 8.9598,
                "mpp_voltage": 38.1285,
                "max_power": 341.6237
            }
        ])

    def test_process_key_iv_points_no_inputs(self):
        self._make_mocked_api()
        module = Module(api=self.mocked_api)

        with self.assertRaises(ValueError) as e:
            module.process_key_iv_points()
        self.assertEqual(e.exception.args[0], "Either a file path to the .xslx template for Key IV Points input or the "
                                              "properly formatted JSON-serializable data structure for Key IV Points "
                                              "input must be assigned as input. See the Python SDK documentation "
                                              "(https://plantpredict-python.readthedocs.io/en/latest/) for more "
                                              "information.")

    def test_process_key_iv_points_conflicting_inputs(self):
        self._make_mocked_api()
        module = Module(api=self.mocked_api)

        with self.assertRaises(ValueError) as e:
            module.process_key_iv_points(
                file_path="fake_file_path.xlsx",
                key_iv_points_data={
                    "temperature": 25,
                    "irradiance": 1000,
                    "short_circuit_current": 9.43,
                    "open_circuit_voltage": 46.39,
                    "mpp_current": 8.9598,
                    "mpp_voltage": 38.1285,
                    "max_power": 341.6237
                }
            )
        self.assertEqual(e.exception.args[0], "Only one input option may be specified.")

    @mock.patch('plantpredict.module.requests.post', new=mocked_requests.mocked_requests_post)
    def test_process_key_iv_points_with_file(self):
        self._make_mocked_api()
        module = Module(api=self.mocked_api)

        response = module.process_key_iv_points(file_path="test_data/test_parse_key_iv_points_template.xlsx")
        self.assertEqual(response.json(), {
            "stc_short_circuit_current": 1.7592,
            "stc_open_circuit_voltage": 90.2189,
            "stc_mpp_current": 1.6084,
            "stc_mpp_voltage": 72.4938,
            "stc_short_circuit_current_temp_coef": 0.0519,
            "stc_open_circuit_voltage_temp_coef": -0.3081,
            "stc_power_temp_coef": -0.3535,
            "effective_irradiance_response": [
                {"temperature": 25, "irradiance": 1000, "relative_efficiency": 1.0},
                {"temperature": 25, "irradiance": 800, "relative_efficiency": 1.0039},
                {"temperature": 25, "irradiance": 600, "relative_efficiency": 1.0032},
                {"temperature": 25, "irradiance": 400, "relative_efficiency": 0.9925},
                {"temperature": 25, "irradiance": 200, "relative_efficiency": 0.9582},
            ]
        })
        self.assertEqual(module.stc_short_circuit_current, 1.7592)
        self.assertEqual(module.effective_irradiance_response, [
                {"temperature": 25, "irradiance": 1000, "relative_efficiency": 1.0},
                {"temperature": 25, "irradiance": 800, "relative_efficiency": 1.0039},
                {"temperature": 25, "irradiance": 600, "relative_efficiency": 1.0032},
                {"temperature": 25, "irradiance": 400, "relative_efficiency": 0.9925},
                {"temperature": 25, "irradiance": 200, "relative_efficiency": 0.9582},
        ])

    @mock.patch('plantpredict.module.requests.post', new=mocked_requests.mocked_requests_post)
    def test_process_key_iv_points_with_data(self):
        self._make_mocked_api()
        module = Module(api=self.mocked_api)

        response = module.process_key_iv_points(key_iv_points_data=[
            {
                "temperature": 25,
                "irradiance": 1000,
                "short_circuit_current": 9.43,
                "open_circuit_voltage": 46.39,
                "mpp_current": 8.9598,
                "mpp_voltage": 38.1285,
                "max_power": 341.6237
            },
            {
                "temperature": 25,
                "irradiance": 1000,
                "short_circuit_current": 9.43,
                "open_circuit_voltage": 46.39,
                "mpp_current": 8.9598,
                "mpp_voltage": 38.1285,
                "max_power": 341.6237
            }
        ])
        self.assertEqual(response.json(), {
            "stc_short_circuit_current": 1.7592,
            "stc_open_circuit_voltage": 90.2189,
            "stc_mpp_current": 1.6084,
            "stc_mpp_voltage": 72.4938,
            "stc_short_circuit_current_temp_coef": 0.0519,
            "stc_open_circuit_voltage_temp_coef": -0.3081,
            "stc_power_temp_coef": -0.3535,
            "effective_irradiance_response": [
                {"temperature": 25, "irradiance": 1000, "relative_efficiency": 1.0},
                {"temperature": 25, "irradiance": 800, "relative_efficiency": 1.0039},
                {"temperature": 25, "irradiance": 600, "relative_efficiency": 1.0032},
                {"temperature": 25, "irradiance": 400, "relative_efficiency": 0.9925},
                {"temperature": 25, "irradiance": 200, "relative_efficiency": 0.9582},
            ]
        })
        self.assertEqual(module.stc_short_circuit_current, 1.7592)
        self.assertEqual(module.effective_irradiance_response, [
                {"temperature": 25, "irradiance": 1000, "relative_efficiency": 1.0},
                {"temperature": 25, "irradiance": 800, "relative_efficiency": 1.0039},
                {"temperature": 25, "irradiance": 600, "relative_efficiency": 1.0032},
                {"temperature": 25, "irradiance": 400, "relative_efficiency": 0.9925},
                {"temperature": 25, "irradiance": 200, "relative_efficiency": 0.9582},
        ])

    @mock.patch('plantpredict.module.requests.post', new=mocked_requests.mocked_requests_post)
    def test_calculate_basic_data_at_conditions(self):
        self._make_mocked_api()
        module = Module(self.mocked_api)

        data = module.calculate_basic_data_at_conditions(temperature=25, irradiance=1000)
        self.assertEqual(data, [
            {
                "temperature": 25,
                "irradiance": 1000,
                "short_circuit_current": 9.43,
                "open_circuit_voltage": 46.39,
                "mpp_current": 8.9598,
                "mpp_voltage": 38.1285,
                "max_power": 341.6237
            },
            {
                "temperature": 25,
                "irradiance": 1000,
                "short_circuit_current": 9.43,
                "open_circuit_voltage": 46.39,
                "mpp_current": 8.9598,
                "mpp_voltage": 38.1285,
                "max_power": 341.6237
            }
        ])

    @mock.patch('plantpredict.module.requests.post', new=mocked_requests.mocked_requests_post)
    def test_calculate_effective_irradiance_response(self):
        self._make_mocked_api()
        module = Module(self.mocked_api)

        response = module.calculate_effective_irradiance_response()
        self.assertEqual(response.json(), [
            {'temperature': 25, 'irradiance': 1000, 'relative_efficiency': 1.0},
            {'temperature': 25, 'irradiance': 800, 'relative_efficiency': 1.02},
            {'temperature': 25, 'irradiance': 600, 'relative_efficiency': 1.001},
            {'temperature': 25, 'irradiance': 400, 'relative_efficiency': 0.99},
            {'temperature': 25, 'irradiance': 200, 'relative_efficiency': 0.97}
        ])

    @mock.patch('plantpredict.module.requests.post', new=mocked_requests.mocked_requests_post)
    def test_generate_single_diode_parameters_advanced(self):
        self._make_mocked_api()
        module = Module(self.mocked_api)

        response = module.generate_single_diode_parameters_advanced()
        self.assertEqual(response.json(), {
            "maximum_series_resistance": 6.0,
            "maximum_recombination_parameter": 2.5,
            "saturation_current_at_stc": 0.0000000012,
            "diode_ideality_factor_at_stc": 1.56,
            "linear_temp_dependence_on_gamma": -0.04,
            "light_generated_current": 1.8
        })
        self.assertEqual(module.diode_ideality_factor_at_stc, 1.56)

    @mock.patch('plantpredict.module.requests.post', new=mocked_requests.mocked_requests_post)
    def test_generate_single_diode_parameters_default(self):
        self._make_mocked_api()
        module = Module(self.mocked_api)

        response = module.generate_single_diode_parameters_default()
        self.assertEqual(response.json(), {
            "maximum_series_resistance": 6.0,
            "maximum_recombination_parameter": 2.5,
            "saturation_current_at_stc": 0.0000000012,
            "diode_ideality_factor_at_stc": 1.78,
            "linear_temp_dependence_on_gamma": -0.04,
            "light_generated_current": 1.8
        })
        self.assertEqual(module.diode_ideality_factor_at_stc, 1.78)

    @mock.patch('plantpredict.module.requests.post', new=mocked_requests.mocked_requests_post)
    def test_optimize_series_resistance(self):
        self._make_mocked_api()
        module = Module(self.mocked_api)

        response = module.optimize_series_resistance()
        self.assertEqual(response.json(), {
            "maximum_series_resistance": 6.0,
            "maximum_recombination_parameter": 2.5,
            "saturation_current_at_stc": 0.0000000012,
            "diode_ideality_factor_at_stc": 1.22,
            "linear_temp_dependence_on_gamma": -0.04,
            "light_generated_current": 1.8
        })
        self.assertEqual(module.diode_ideality_factor_at_stc, 1.22)


if __name__ == '__main__':
    unittest.main()
