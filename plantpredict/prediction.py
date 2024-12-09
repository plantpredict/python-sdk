import requests
import json

from plantpredict.plant_predict_entity import PlantPredictEntity
from plantpredict.utilities import convert_json, snake_to_camel, camel_to_snake
from plantpredict.error_handlers import handle_refused_connection, handle_error_response, APIError
from plantpredict.enumerations import PredictionStatusEnum, EntityTypeEnum


class Prediction(PlantPredictEntity):
    """
    The :py:mod:`plantpredict.Prediction` entity models a single energy prediction within a
    :py:mod:`plantpredict.Project`.
    """
    def create(self, use_closest_ashrae_station=True, error_spa_var=2.0, error_model_acc=2.9, error_int_ann_var=3.0,
               error_sens_acc=5.0, error_mon_acc=2.0, year_repeater=1, status=PredictionStatusEnum.DRAFT_PRIVATE):
        """
        **POST** */Project/ :py:attr:`project_id` /Prediction*

        Creates a new :py:mod:`plantpredict.Prediction` entity in the PlantPredict database using the attributes
        assigned to the local object instance. Automatically assigns the resulting :py:attr:`id` to the local object
        instance. See the minimum required attributes (below) necessary to successfully create a new
        :py:mod:`plantpredict.Prediction`. Note that the full scope of attributes is not limited to the minimum
        required set. **Important Note:** the minimum required attributes necessary to create a
        :py:mod:`plantpredict.Prediction` is not sufficient to successfully call :py:meth:`plantpredict.Prediction.run`.

        .. container:: toggle

            .. container:: header

                **Required Attributes**

            .. container:: required_attributes

                .. csv-table:: Minimum required attributes for successful Prediction creation
                    :delim: ;
                    :header: Field, Type, Description
                    :stub-columns: 1

                    name; str; Name of prediction
                    project_id; int; ID of project within which to contain the prediction
                    year_repeater; int; Must be between :py:data:`1` and :py:data:`50` - unitless.

        .. container:: toggle

            .. container:: header

                **Example Code**

            .. container:: example_code

                First, import the plantpredict library and receive an authentication api.access_token in your
                Python session, as shown in Step 3 of :ref:`authentication_oauth2`. Then instantiate a local Prediction.
                object.

                .. code-block:: python

                    module_to_create = plantpredict.Prediction()

                Populate the Prediction's require attributes by either directly assigning them...

                .. code-block:: python

                    from plantpredict.enumerations import PredictionStatusEnum

                    prediction_to_create.name = "Test Prediction"
                    prediction_to_create.project_id = 1000
                    prediction_to_create.status = PredictionStatusEnum.DRAFT_SHARED
                    prediction_to_create.year_repeater = 1

                ...OR via dictionary assignment.

                .. code-block:: python

                    prediction_to_create.__dict__ = {
                        "name": "Test Prediction",
                        "model": "Test Module",
                        "status": PredictionStatusEnum.DRAFT_SHARED,
                        "year_repeater": 1,
                    }

                Create a new prediction in the PlantPredict database, and observe that the Module now has a unique
                database identifier.

                .. code-block:: python

                    prediction_to_create.create()

                    print(prediction_to_create.id)

        :return: A dictionary containing the prediction id.
        :rtype: dict
        """

        self.create_url_suffix = "/Project/{}/Prediction".format(self.project_id)

        self.error_spa_var = error_spa_var
        self.error_model_acc = error_model_acc
        self.error_int_ann_var = error_int_ann_var
        self.error_sens_acc = error_sens_acc
        self.error_mon_acc = error_mon_acc
        self.year_repeater = year_repeater
        self.status = status

        if use_closest_ashrae_station:
            self._assign_plant_design_temperature_with_closest_ashrae_station()

        return super(Prediction, self).create()

    def _assign_plant_design_temperature_with_closest_ashrae_station(self):
        """
        Assigns the plant design temperatures by using the closest ASHRAE station (based on the associated project's
        latitude and longitude).
        """
        project = self.api.project(id=self.project_id)
        project.get()
        ashrae = self.api.ashrae(latitude=project.latitude, longitude=project.longitude)

        ashrae.get_closest_station()

        # set relevant attributes from ASHRAE to Prediction
        self.ashrae_station = ashrae.station_name
        self.cool_996 = ashrae.cool_996
        self.max_50_year = ashrae.max_50_year
        self.min_50_year = ashrae.min_50_year

    def delete(self):
        """HTTP Request: DELETE /Project/{ProjectId}/Prediction/{Id}

        Deletes an existing Prediction entity in PlantPredict. The local instance of the Project entity must have
        attribute self.id identical to the prediction id of the Prediction to be deleted.

        :return: A dictionary {"is_successful": True}.
        :rtype: dict
        """
        self.delete_url_suffix = "/Project/{}/Prediction/{}".format(self.project_id, self.id)

        return super(Prediction, self).delete()

    def get(self, id=None, project_id=None):
        """HTTP Request: GET /Project/{ProjectId}/Prediction/{Id}

        Retrieves an existing Prediction entity in PlantPredict and automatically assigns all of its attributes to the
        local Prediction object instance. The local instance of the Prediction entity must have attribute self.id
        identical to the prediction id of the Prediction to be retrieved.

        :return: A dictionary containing all of the retrieved Prediction attributes.
        :rtype: dict

        """
        self.id = id if id is not None else self.id
        self.project_id = project_id if project_id is not None else self.project_id

        self.get_url_suffix = "/Project/{}/Prediction/{}".format(self.project_id, self.id)

        return super(Prediction, self).get()

    def update(self):
        """HTTP Request: PUT /Project/{ProjectId}/Prediction

        Updates an existing Prediction entity in PlantPredict using the full attributes of the local Prediction
        instance. Calling this method is most commonly preceded by instantiating a local instance of Prediction with a
        specified prediction id, calling the Prediction.get() method, and changing any attributes locally.

        :return: A dictionary {"is_successful": True}.
        :rtype: dict
        """

        self.update_url_suffix = "/Project/{}/Prediction".format(self.project_id)

        return super(Prediction, self).update()

    @handle_refused_connection
    def _wait_for_prediction(self):
        is_complete = False
        while not is_complete:
            self.get()
            if self.processing_status == 3:
                is_complete = True

    @handle_refused_connection
    @handle_error_response
    def run(self, export_options=None):
        """
        POST /Project/{ProjectId}/Prediction/{PredictionId}/Run

        Runs the Prediction and waits for simulation to complete. The input variable "export_options" should take the

        :param export_options: Contains options for exporting
        :return:
        """
        response = requests.post(
            url=self.api.base_url + "/Project/{}/Prediction/{}/Run".format(self.project_id, self.id),
            headers={"Authorization": "Bearer " + self.api.access_token},
            json=convert_json(export_options, snake_to_camel) if export_options else None
        )
        # TODO why didn't this return an error? it only returned when I stopped the script

        # observes task queue to wait for prediction run to complete
        self._wait_for_prediction()

        return response

    @handle_refused_connection
    @handle_error_response
    def get_results_summary(self, negate_losses=False):
        """GET /Project/{ProjectId}/Prediction/{Id}/ResultSummary"""

        response = requests.get(
            url=self.api.base_url + "/Project/{}/Prediction/{}/ResultSummary".format(self.project_id, self.id),
            headers={"Authorization": "Bearer " + self.api.access_token}
        )
        if not response.status_code == 200:
            raise APIError(response.status_code, response.content, response.url)

        if negate_losses:
            results = json.loads(response.content)
            for year in results['years']:
                for factor in year['monthlyFactors']:
                    factor['soilingLoss'] *= -1
                    if factor['spectralShift'] is not None:
                        factor['spectralShift'] *= -1

                for ttl in year['transformerTransmissionLineLoss']:
                    ttl['loss'] *= -1

                year['transpositionOnPlane'] *= -1
                year['farShadingLoss'] *= -1
                year['nearShadingLoss'] *= -1
                year['elecShadingLoss'] *= -1
                year['soilingLoss'] *= -1
                year['iamFactorLoss'] *= -1
                year['spectralLoss'] *= -1
                year['moduleIrradianceLoss'] *= -1
                year['moduleTemperatureLoss'] *= -1
                year['moduleQualityLoss'] *= -1
                year['lidLoss'] *= -1
                year['moduleMismatchLoss'] *= -1
                year['moduleBackMismatchLoss'] *= -1
                year['biFacialityLoss'] *= -1
                year['structureShadingLoss'] *= -1
                year['backsideIrradiance'] *= -1
                year['dcWiringLoss'] *= -1
                year['dcHealthLoss'] *= -1
                year['inverterEfficiencyLoss'] *= -1
                year['inverterLimitationLoss'] *= -1
                year['degradationLoss'] *= -1
                year['leTIDLoss'] *= -1
                year['inverterCoolingLoss'] *= -1
                year['trackerMotorLoss'] *= -1
                year['dataAcquisitionAuxLoss'] *= -1
                year['mvTransformersLoss'] *= -1
                year['acCollectionLinesLoss'] *= -1
                year['availabilityLoss'] *= -1
                year['lgiaLimitationLoss'] *= -1

            # convert_json(response.json(), camel_to_snake)
            return convert_json(results, camel_to_snake)

        return response

    @handle_refused_connection
    @handle_error_response
    def get_results_details(self):
        """GET /Project/{ProjectId}/Prediction/{Id}/ResultDetails"""

        response = requests.get(
            url=self.api.base_url + "/Project/{}/Prediction/{}/ResultDetails".format(self.project_id, self.id),
            headers={"Authorization": "Bearer " + self.api.access_token}
        )
        if not response.status_code == 200:
            raise APIError(response.status_code, response.content, response.url)

        return response

    @handle_refused_connection
    @handle_error_response
    def get_nodal_data(self, params=None):
        """GET /Project/{ProjectId}/Prediction/{Id}/NodalJson"""

        response = requests.get(
            url=self.api.base_url + "/Project/{}/Prediction/{}/NodalJson".format(self.project_id, self.id),
            headers={"Authorization": "Bearer " + self.api.access_token},
            params=convert_json(params, snake_to_camel) if params else {}
        )
        if not response.status_code == 200:
            raise APIError(response.status_code, response.content, response.url)
        return response

    @handle_refused_connection
    @handle_error_response
    def clone(self, new_prediction_name):
        """

        :param new_prediction_name:
        :return:
        """
        new_prediction = self.api.prediction()
        self.get()
        original_prediction_id = self.id

        new_prediction.__dict__ = self.__dict__
        # initialize necessary fields
        new_prediction.__dict__.pop('id', None)
        new_prediction.__dict__.pop('created_date', None)
        new_prediction.__dict__.pop('last_modified', None)
        new_prediction.__dict__.pop('last_modified_by', None)
        new_prediction.__dict__.pop('last_modified_by_id', None)
        new_prediction.__dict__.pop('project', None)
        new_prediction.__dict__.pop('powerplant_id', None)
        new_prediction.__dict__.pop('powerplant', None)

        new_prediction.name = new_prediction_name
        new_prediction.create()
        new_prediction_id = new_prediction.id

        # clone powerplant and attach to new prediction
        new_powerplant = self.api.powerplant()
        powerplant = self.api.powerplant(project_id=self.project_id, prediction_id=original_prediction_id)
        powerplant.get()
        new_powerplant.__dict__ = powerplant.__dict__
        new_powerplant.prediction_id = new_prediction_id
        new_powerplant.__dict__.pop('id', None)

        # initialize necessary fields
        for block in new_powerplant.blocks:
            block.pop('id', None)
            for array in block['arrays']:
                array.pop('id', None)
                for inverter in array['inverters']:
                    inverter.pop('id', None)
                    for dc_field in inverter['dc_fields']:
                        dc_field.pop('id', None)

        new_powerplant.create()

        self.id = original_prediction_id
        self.get()

        return new_prediction_id

    @handle_refused_connection
    @handle_error_response
    def change_status(self, new_status, note=""):
        """
        Change the status (and resulting sharing/privacy settings) of a prediction (ex. from py:attr:`DRAFT_PRIVATE` to
        py:attr:`DRAFT-SHARED`.

        :param int new_status: Enumeration representing status to change prediction to. See (or import)
                               :py:class:`plantpredict.enumerations.PredictionStatusEnum`.
        :param str note: Description of reason for change.
        :return:
        """
        return requests.post(
            url=self.api.base_url + "/Project/{}/Prediction/Status".format(self.project_id),
            headers={"Authorization": "Bearer " + self.api.access_token},
            json=[{
                "name": self.name,
                "id": self.id,
                "type": EntityTypeEnum.PREDICTION,
                "status": new_status,
                "note": note
            }]
        )
    @handle_refused_connection
    @handle_error_response
    def get_time_series_data(self):
        """
        GET /Project/{ProjectId}/Prediction/{PredictionId}/TimeSeriesData

        :return:
        """
        return requests.get(
            url=self.api.base_url + "/Project/{}/Prediction/{}/TimeSeriesData".format(self.project_id, self.id),
            headers={"Authorization": "Bearer " + self.api.access_token}
        )

    @handle_refused_connection
    @handle_error_response
    def get_time_series_details(self, time_series_id):
        """
        GET /Project/{ProjectId}/Prediction/{PredictionId}/TimeSeriesData/{TimeSeriesId}

        :param time_series_id:
        :return:
        """
        request = requests.get(
            url=self.api.base_url + "/Project/{}/Prediction/{}/TimeSeriesData/{}/Details".format(self.project_id, self.id, time_series_id),
            headers={"Authorization": "Bearer " + self.api.access_token}
        )

        return json.loads(request.content)
    @handle_refused_connection
    @handle_error_response
    def add_time_series_json(self, time_series_json):
        """
        POST /Project/{ProjectId}/Prediction/{PredictionId}/TimeSeriesData

        :param time_series_json:
        :return:
        """
        return requests.post(
            url=self.api.base_url + "/Project/{}/Prediction/{}/TimeSeriesData".format(self.project_id, self.id),
            headers={"Authorization": "Bearer " + self.api.access_token},
            json=time_series_json
        )

    @handle_refused_connection
    @handle_error_response
    def delete_time_series_data(self, time_series_id):
        """
        DELETE /Project/{ProjectId}/Prediction/{PredictionId}/TimeSeriesData/{TimeSeriesId}

        :param time_series_id:
        :return:
        """
        return requests.delete(
            url=self.api.base_url + "/Project/{}/Prediction/{}/TimeSeriesData/{}".format(self.project_id, self.id, time_series_id),
            headers={"Authorization": "Bearer " + self.api.access_token}
        )

    def __init__(self, api, id=None, project_id=None, name=None):
        if id:
            self.id = id
        self.project_id = project_id
        self.name = name

        self.status = None
        self.year_repeater = None

        self.error_spa_var = None
        self.error_model_acc = None
        self.error_int_ann_var = None
        self.error_sens_acc = None
        self.error_mon_acc = None

        super(Prediction, self).__init__(api)
