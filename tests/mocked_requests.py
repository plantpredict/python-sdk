import json

from plantpredict.enumerations import ModuleOrientationEnum, FacialityEnum


class MockResponse:
    def __init__(self, status_code, json_data=None, content=None):
        self.content = json.dumps(json_data) if json_data else content
        self.status_code = status_code

    def json(self):
        return self.content


def mocked_requests_post(*args, **kwargs):
    if kwargs['url'] == "https://afse.okta.com/oauth2/aus3jzhulkrINTdnc356/v1/token":
        if kwargs["params"]["grant_type"] == "password":
            return MockResponse(
                json_data={"access_token": "dummy access token", "refresh_token": "dummy refresh token"},
                status_code=200
            )

        elif kwargs["params"]["grant_type"] == "refresh_token":
            return MockResponse(
                json_data={"access_token": "dummy access token 2", "refresh_token": "dummy refresh token 2"},
                status_code=200
            )

    elif kwargs['url'] == "https://api.plantpredict.com/create-info/80206":
        return MockResponse(
            json_data={"id": 35},
            status_code=200
        )

    elif kwargs['url'] == "https://api.plantpredict.com/Project/710/Prediction/556/PowerPlant":
        return MockResponse(
            json_data={},
            status_code=204
        )

    elif kwargs['url'] == "https://api.plantpredict.com/Project/710/Prediction/555/Run":
        return MockResponse(json_data={}, status_code=204)

    elif kwargs['url'] == "https://api.plantpredict.com/Project/710/Prediction/555/ResultSummary":
        return MockResponse(
            json_data={},
            status_code=200
        )

    elif kwargs['url'] == "https://api.plantpredict.com/Project/710/Prediction":
        return MockResponse(
            json_data={"id": 556, "project_id": 710, "name": "Prediction Name 2"},
            status_code=200
        )

    elif kwargs['url'] == "https://api.plantpredict.com/Weather/Download/1" and kwargs['params'] == {
        'latitude': 39.67, 'longitude': -105.21
    }:
        return MockResponse(
            json_data={"id": 997, "name": "Downloaded Weather File"},
            status_code=200
        )

    elif kwargs['url'] == "https://api.plantpredict.com/Module/Generator/GenerateIVCurve":
        return [{"current": 1.2, "voltage": 100.0}]

    elif kwargs['url'] == "https://api.plantpredict.com/Module/Generator/ProcessIVCurves":
        return MockResponse(json_data=[
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
        ], status_code=200)

    elif kwargs['url'] == "https://api.plantpredict.com/Module/Generator/ProcessKeyIVPoints":
        return MockResponse(json_data={
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
        }, status_code=200)

    elif kwargs['url'] == "https://api.plantpredict.com/Module/Generator/CalculateEffectiveIrradianceResponse":
        return MockResponse(json_data=[
            {'temperature': 25, 'irradiance': 1000, 'relative_efficiency': 1.0},
            {'temperature': 25, 'irradiance': 800, 'relative_efficiency': 1.02},
            {'temperature': 25, 'irradiance': 600, 'relative_efficiency': 1.001},
            {'temperature': 25, 'irradiance': 400, 'relative_efficiency': 0.99},
            {'temperature': 25, 'irradiance': 200, 'relative_efficiency': 0.97}
        ], status_code=200)

    elif kwargs['url'] == "https://api.plantpredict.com/Module/Generator/GenerateSingleDiodeParametersAdvanced":
        return MockResponse(json_data={
            "maximum_series_resistance": 6.0,
            "maximum_recombination_parameter": 2.5,
            "saturation_current_at_stc": 0.0000000012,
            "diode_ideality_factor_at_stc": 1.56,
            "linear_temp_dependence_on_gamma": -0.04,
            "light_generated_current": 1.8
        }, status_code=200)

    elif kwargs['url'] == "https://api.plantpredict.com/Module/Generator/GenerateSingleDiodeParametersDefault":
        return MockResponse(json_data={
            "maximum_series_resistance": 6.0,
            "maximum_recombination_parameter": 2.5,
            "saturation_current_at_stc": 0.0000000012,
            "diode_ideality_factor_at_stc": 1.78,
            "linear_temp_dependence_on_gamma": -0.04,
            "light_generated_current": 1.8
        }, status_code=200)

    elif kwargs['url'] == "https://api.plantpredict.com/Module/Generator/OptimizeSeriesResistance":
        return MockResponse(json_data={
            "maximum_series_resistance": 6.0,
            "maximum_recombination_parameter": 2.5,
            "saturation_current_at_stc": 0.0000000012,
            "diode_ideality_factor_at_stc": 1.22,
            "linear_temp_dependence_on_gamma": -0.04,
            "light_generated_current": 1.8
        }, status_code=200)

    return MockResponse(None, 404)


def mocked_requests_get(*args, **kwargs):
    if kwargs['url'] == "https://api.plantpredict.com/Geo/39.67/-105.21/Location":
        return MockResponse(
            json_data={
                "country": "United States",
                "country_code": "US",
                "locality": "Morrison",
                "region": "North America",
                "state_province": "Colorado",
                "state_province_code": "CO"
            },
            status_code=200
        )

    elif kwargs['url'] == "https://api.plantpredict.com/Geo/39.67/-105.21/Elevation":
        return MockResponse(
            json_data={"elevation": 1965.96},
            status_code=200
        )

    elif kwargs['url'] == "https://api.plantpredict.com/Geo/39.67/-105.21/TimeZone":
        return MockResponse(
            json_data={"time_zone": -7.0},
            status_code=200
        )

    elif kwargs['url'] == "https://api.plantpredict.com/Module/123":
        return MockResponse(
            json_data={
                "default_orientation": ModuleOrientationEnum.LANDSCAPE,
                "length": 2000,
                "width": 1200,
                "stc_max_power": 120,
                "sandia_conductive_coef": 30.7,
                "sandia_convective_coef": 0.0,
                "cell_to_module_temp_diff": 3.0,
                "heat_balance_conductive_coef": -3.47,
                "heat_balance_convective_coef": -0.0594,
                "module_mismatch_coefficient": 1.0,
                "module_quality": 1.0,
                "light_induced_degradation": 1.0,
                "faciality": FacialityEnum.MONOFACIAL
            },
            status_code=200
        )

    elif kwargs['url'] == "https://api.plantpredict.com/Module/456":
        return MockResponse(
            json_data={
                "default_orientation": ModuleOrientationEnum.LANDSCAPE,
                "length": 2000,
                "width": 1200,
                "stc_max_power": 120,
                "sandia_conductive_coef": 30.7,
                "sandia_convective_coef": 0.0,
                "cell_to_module_temp_diff": 3.0,
                "heat_balance_conductive_coef": -3.47,
                "heat_balance_convective_coef": -0.0594,
                "module_mismatch_coefficient": 1.0,
                "module_quality": 1.0,
                "light_induced_degradation": 1.0,
                "faciality": FacialityEnum.BIFACIAL,
                "backside_mismatch": 3.0,
            },
            status_code=200
        )

    elif kwargs['url'] == "https://api.plantpredict.com/get-info/80206":
        return MockResponse(
            json_data={"color": "blue"},
            status_code=200
        )

    elif kwargs['url'] == "https://api.plantpredict.com/get-info/80207":
        return MockResponse(
            content="Info not found.",
            status_code=404
        )

    elif kwargs['url'] == "https://api.plantpredict.com/Project/710/Prediction/555/PowerPlant":
        return MockResponse(
            json_data={
                "id": 1000,
                "project_id": 710,
                "prediction_id": 555,
                "blocks": [{
                    "id": 1,
                    "arrays": [{
                        "id": 2,
                        "inverters": [{
                            "id": 3,
                            "dc_fields": [{"id": 4}]
                        }]
                    }]
                }]
            },
            status_code=200
        )

    elif kwargs['url'] == "https://api.plantpredict.com/Project/710/Prediction/555/ResultSummary":
        return MockResponse(
            json_data={"prediction_name": "Test Prediction", "block_result_summaries": [{"name": 1}]},
            status_code=200
        )

    elif kwargs['url'] == "https://api.plantpredict.com/Project/710/Prediction/555/ResultDetails":
        return MockResponse(
            json_data={"prediction_name": "Test Prediction Details"},
            status_code=200
        )

    elif kwargs['url'] == "https://api.plantpredict.com/Project/710/Prediction/555/NodalJson":
        return {"nodal_data_dc_field": {}}

    elif kwargs['url'] == "https://api.plantpredict.com/Project/710/Prediction/555":
        return MockResponse(
            json_data={"id": 555, "project_id": 710, "name": "Prediction Name"},
            status_code=200
        )

    elif kwargs['url'] == "https://api.plantpredict.com/Project/710/Prediction":
        return MockResponse(
            json_data=[
                {"project_id": 1, "name": "Project 1"},
                {"project_id": 2, "name": "Project 2"},
                {"project_id": 3, "name": "Project 3"}
            ],
            status_code=200
        )

    elif kwargs['url'] == "https://api.plantpredict.com/Project/Search":
        return MockResponse(
            json_data=[{"project_id": 1, "name": "Project 1"}],
            status_code=200
        )

    elif kwargs['url'] == "https://api.plantpredict.com/Project/7":
        return MockResponse(
            json_data={"latitude": 33.0, "longitude": -110.0},
            status_code=200
        )

    elif kwargs['url'] == "https://api.plantpredict.com/Project/8":
        return MockResponse(
            json_data={"latitude": -33.0, "longitude": -110.0},
            status_code=200
        )

    elif kwargs['url'] == "https://api.plantpredict.com/Weather/999/Detail":
        return MockResponse(
            json_data={"id": 999, "name": "Weather File"},
            status_code=200
        )

    elif kwargs['url'] == "https://api.plantpredict.com/Weather/Search" and kwargs['params'] == {
        'latitude': 39.67, 'longitude': -105.21, 'searchRadius': 1
    }:
        return MockResponse(
            json_data=[{"id": 998, "name": "Weather File 2"}],
            status_code=200
        )

    elif kwargs['url'] == "https://api.plantpredict.com/ASHRAE/GetStation" and kwargs['params'] == {
        'latitude': 35.0, 'longitude': -109.0, 'stationName': 'TEST STATION'
    }:
        return MockResponse(
            json_data={
                "station_name": "TEST STATION",
                "wmo": 18081,
                "cool_996": 20.0,
                "min_50_year": -20.0,
                "max_50_year": 17.0,
                "distance": 5.3,
                "latitude": 35.0,
                "longitude": -109.0
            },
            status_code=200
        )

    elif kwargs['url'] == "https://api.plantpredict.com/ASHRAE" and kwargs['params'] == {
        'latitude': 33.0, 'longitude': -110.0
    }:
        return MockResponse(
            json_data={
                "station_name": "TEST STATION",
                "wmo": 18081,
                "cool_996": 20.0,
                "min_50_year": -20.0,
                "max_50_year": 17.0,
                "distance": 5.3,
                "latitude": 35.0,
                "longitude": -109.0
            },
            status_code=200
        )

    elif kwargs['url'] == "https://api.plantpredict.com/Inverter/808/kVa" and kwargs['params'] == {
        'elevation': 1000, 'temperature': 20.0, 'useCoolingTemp': True
    }:
        return MockResponse(
            json_data={'kva': 700.0},
            status_code=200
        )

    elif kwargs['url'] == "https://api.plantpredict.com/Inverter/808/":
        return MockResponse(
            json_data={'power_rated': 600.0},
            status_code=200
        )

    return MockResponse(None, 404)


def mocked_requests_delete(*args, **kwargs):
    if kwargs['url'] == "https://api.plantpredict.com/delete-info/80206":
        return MockResponse(
            json_data={"success": True},
            status_code=200
        )

    return MockResponse(None, 404)


def mocked_requests_update(*args, **kwargs):
    if kwargs['url'] == "https://api.plantpredict.com/update-info/80206":
        return MockResponse(
            json_data={"color": "red"},
            status_code=200
        )

    return MockResponse(None, 404)
