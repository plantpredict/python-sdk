import json
import requests

from plantpredict.utilities import convert_json, camel_to_snake, decorate_all_methods
from plantpredict.error_handlers import handle_refused_connection, handle_error_response, APIError


@decorate_all_methods(handle_refused_connection)
@decorate_all_methods(handle_error_response)
class ASHRAE(object):
    """
    The :py:class:`~plantpredict.ashrae.ASHRAE` class is used to get key information for an ASHRAE station. It can be
    used on its own for any application, but mostly exists to find and assign plant design temperatures for a particular
    location to a :py:class:`~plantpredict.prediction.Prediction`.
    """
    def get_station(self, station_name=None):
        """
        Returns the ASHRAE station matching the specified name and shortest distance from the specified latitude and
        longitude. Sets the returned information as attributes on the instance of this class.

        :param str station_name: Valid name of ASHRAE weather station
        :return: # TODO once new http response is implemented
        """
        self.station_name = station_name if station_name else self.station_name
        response = requests.get(
            url=self.api.base_url + "/ASHRAE/GetStation",
            headers={"Authorization": "Bearer " + self.api.access_token},
            params={"latitude": self.latitude, "longitude": self.longitude, "stationName": self.station_name}
        )
        if not response.status_code == 200:
            raise APIError(response.status_code, response.content, response.url)

        attr = convert_json(response.json(), camel_to_snake)
        for key in attr:
            setattr(self, key, attr[key])

        return response

    def get_closest_station(self):
        """
        Returns the ASHRAE station with the shortest distance from the specified latitude and longitude. Sets the
        returned information as attributes on the instance of this class.

        :return: # TODO once new http response is implemented
        """
        response = requests.get(
            url=self.api.base_url + "/ASHRAE",
            headers={"Authorization": "Bearer " + self.api.access_token},
            params={"latitude": self.latitude, "longitude": self.longitude}
        )
        if not response.status_code == 200:
            raise APIError(response.status_code, response.content, response.url)

        attr = convert_json(response.json(), camel_to_snake)
        for key in attr:
            setattr(self, key, attr[key])

        return response

    def __init__(self, api, latitude=None, longitude=None, station_name=None):
        self.api = api
        self.latitude = latitude
        self.longitude = longitude
        self.station_name = station_name

        super(ASHRAE, self).__init__()
