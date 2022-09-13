import requests
import json

from plantpredict.plant_predict_entity import PlantPredictEntity
from plantpredict.error_handlers import handle_refused_connection, handle_error_response
from plantpredict.utilities import convert_json, camel_to_snake


class Project(PlantPredictEntity):
    """
    The Project entity in PlantPredict defines the location info and serves as a container for any number of Predictions.
    """
    def create(self):
        """
        **POST** */Project/*

        Creates a new :py:mod:`plantpredict.Project` entity in the PlantPredict database using the attributes
        assigned to the local object instance. Automatically assigns the resulting :py:attr:`id` to the local object
        instance. See the minimum required attributes (below) necessary to successfully create a new
        :py:mod:`plantpredict.Project`. Note that the full scope of attributes is not limited to the minimum
        required set.

        Use :py:meth:`plantpredict.Project.assign_location_attributes` to automatically assign all required (and
        non-required) location-related/geological attributes.

        .. container:: toggle

            .. container:: header

                **Required Attributes**

            .. container:: required_attributes

                .. csv-table:: Minimum required attributes for successful Prediction creation
                    :delim: ;
                    :header: Field, Type, Description
                    :stub-columns: 1

                    name; str; Name of the project
                    latitude; float; North-South GPS coordinate of the Project location. Must be between :py:data:`-90` and :py:data:`90` - units :py:data:`[decimal degrees]`.
                    longitude; float; East-West coordinate of the Project location, in decimal degrees. Must be between :py:data:`-180` and :py:data:`180` units :py:data:`[decimal degrees]`.
                    country; str; Full name of the country of the Project's location.
                    country_code; str; Country code of the Project's location (ex. US for United States, AUS for Australia, etc.)
                    elevation; float; The elevation of the Project location above seal level units :py:data:`[m]`.
                    standard_offset_from_utc; float; Time zone with respect to Greenwich Mean Time (GMT) in +/- hours offset.
        """
        self.create_url_suffix = "/Project"

        return super(Project, self).create()

    def delete(self):
        """HTTP Request: DELETE /Project/{ProjectId}

        Deletes an existing Project entity in PlantPredict. The local instance of the Project entity must have
        attribute self.id identical to the project id of the Project to be deleted.

        :return: A dictionary {"is_successful": True}.
        :rtype: dict
        """

        self.delete_url_suffix = "/Project/{}".format(self.id)

        return super(Project, self).delete()

    def get(self):
        """HTTP Request: GET /Project/{Id}

        Retrieves an existing Project entity in PlantPredict and automatically assigns all of its attributes to the
        local Project object instance. The local instance of the Project entity must have attribute self.id identical
        to the project id of the Project to be retrieved.

        :return: A dictionary containing all of the retrieved Project attributes.
        :rtype: dict
        """

        self.get_url_suffix = "/Project/{}".format(self.id)

        return super(Project, self).get()

    def update(self):
        """HTTP Request: PUT /Project

        Updates an existing Project entity in PlantPredict using the full attributes of the local Project instance.
        Calling this method is most commonly preceded by instantiating a local instance of Project with a specified
        project id, calling the Project.get() method, and changing any attributes locally.

        :return: A dictionary {"is_successful": True}.
        :rtype: dict
        """
        self.update_url_suffix = "/Project"

        return super(Project, self).update()

    @handle_refused_connection
    @handle_error_response
    def get_all_predictions(self):
        """HTTP Request: GET /Project/{ProjectId}/Prediction

        Retrieves the full attributes of every Prediction associated with the Project.

        :return: A list of dictionaries, each containing the attributes of a Prediction entity.
        :rtype: list of dict
        """

        return requests.get(
            url=self.api.base_url + "/Project/{}/Prediction".format(self.id),
            headers={"Authorization": "Bearer " + self.api.access_token}
        )

    def search(self, latitude, longitude, search_radius=1.0):
        """HTTP Request: GET /Project/Search

        Searches for all existing Project entities within a search radius of a specified latitude/longitude.

        :param latitude: North-South coordinate of the Project location, in decimal degrees.
        :type latitude: float
        :param longitude: East-West coordinate of the Project location, in decimal degrees.
        :type longitude: float
        :param search_radius: search radius in miles
        :type search_radius: float
        :return: TODO
        """
        response = requests.get(
            url=self.api.base_url + "/Project/Search",
            headers={"Authorization": "Bearer " + self.api.access_token},
            params={'latitude': latitude, 'longitude': longitude, 'searchRadius': search_radius}
        )

        project_list = response.json()

        return [convert_json(p, camel_to_snake) for p in project_list]

    @handle_refused_connection
    @handle_error_response
    def assign_location_attributes(self):
        """

        :return:
        """
        geo = self.api.geo(latitude=self.latitude, longitude=self.longitude)
        geo.get_location_info()
        geo.get_elevation()
        geo.get_time_zone()

        self.locality = geo.locality
        self.state_province_code = geo.state_province_code
        self.state_province = geo.state_province
        self.country_code = geo.country_code
        self.country = geo.country
        self.region = geo.region
        self.elevation = geo.elevation
        self.standard_offset_from_utc = geo.time_zone

    def __init__(self, api, id=None, name=None, latitude=None, longitude=None):
        if id:
            self.id = id
        self.name = name
        self.latitude = latitude
        self.longitude = longitude

        self.locality = None
        self.state_province_code = None
        self.state_province = None
        self.country_code = None
        self.country = None
        self.region = None
        self.elevation = None
        self.standard_offset_from_utc = None

        super(Project, self).__init__(api)
