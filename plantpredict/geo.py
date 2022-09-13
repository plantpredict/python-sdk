import json
import requests
from plantpredict.utilities import convert_json, camel_to_snake, decorate_all_methods
from plantpredict.error_handlers import handle_refused_connection, handle_error_response


@decorate_all_methods(handle_refused_connection)
@decorate_all_methods(handle_error_response)
class Geo(object):
    """
    The :py:mod:`Geo` entity is used to get location-related information for a given latitude/longitude. Its methods can
    be used individually, but typically location related info is needed in the context of a PlantPredict
    :py:mod:`Project` entity. In this case the user can simply call the method :py:meth:`Project.get_location_info`
    which calls all :py:mod:`Geo` class methods and automatically assigns all location-related attributes to that
    instance of :py:mod:`Project`. Note: This API resource does not represent a database entity in PlantPredict. This
    is a simplified connection to the Google Maps API. See Google Maps API Reference for further functionality.
    (https://developers.google.com/maps/)
    """

    def get_location_info(self):
        """
        **GET** */Geo/* :py:attr:`latitude` */* :py:attr:`longitude` */Location*

        Retrieves pertinent location info for a given latitude and longitude such as locality, state/province, country,
        etc. In addition to returning a dictionary with this information, the method also automatically assigns the
        contents of the dictionary to the instance of :py:mod:`Geo` as attributes.

        .. container:: toggle

            .. container:: header

                **Required Attributes**

            .. container:: required_attributes

                .. csv-table:: Minimum required attributes on object to call this method successfully.
                    :delim: ;
                    :header: Field, Type, Description
                    :stub-columns: 1

                    latitude; float; North-South GPS coordinate. Must be between :py:data:`-90` and :py:data:`90` - units :py:data:`[decimal degrees]`.
                    longitude; float; East-West GPS coordinate Must be between :py:data:`-180` and :py:data:`180` units :py:data:`[decimal degrees]`.

        .. container:: toggle

            .. container:: header

                **Example Code**

            .. container:: example_code

                Instantiate a local object instance of :py:mod:`Geo` with latitude and longitude as inputs (which
                automatically assigns them as attributes to the object). Then call the method on the object.

                .. code-block:: python

                    geo = api.geo(latitude=35.1, longitude=-106.7)
                    geo.get_location_info()

        .. container:: toggle

            .. container:: header

                **Example Response**

            .. container:: example_response

                The method returns a dictionary as shown in the example below, and assigns its contents as attributes
                to the local object instance of :py:mod:`Geo`.

                .. code-block:: python

                    {
                        "country": "United States",
                        "country_code": "US",
                        "locality": "Albuquerque",
                        "region": "North America",
                        "state_province": "New Mexico",
                        "state_province_code": "NM
                    }

        :return: A dictionary with location information as shown in "Example Response".
        :rtype: dict
        """
        response = requests.get(
            url=self.api.base_url + "/Geo/{}/{}/Location".format(self.latitude, self.longitude),
            headers={"Authorization": "Bearer " + self.api.access_token}
        )
        attr = convert_json(response.json(), camel_to_snake)
        for key in attr:
            setattr(self, key, attr[key])

        return response

    def get_elevation(self):
        """
        **GET** */Geo/* :py:attr:`latitude` */* :py:attr:`longitude` */Elevation*

        Retrieves the elevation in meters for a given latitude and longitude. In addition to returning a dictionary with
        this information, the method also automatically assigns the  contents of the dictionary to the instance of
        :py:mod:`Geo` as attributes.

        .. container:: toggle

            .. container:: header

                **Required Attributes**

            .. container:: required_attributes

                .. csv-table:: Minimum required attributes on object to call this method successfully.
                    :delim: ;
                    :header: Field, Type, Description
                    :stub-columns: 1

                    latitude; float; North-South GPS coordinate. Must be between :py:data:`-90` and :py:data:`90` - units :py:data:`[decimal degrees]`.
                    longitude; float; East-West GPS coordinate Must be between :py:data:`-180` and :py:data:`180` units :py:data:`[decimal degrees]`.

        .. container:: toggle

            .. container:: header

                **Example Code**

            .. container:: example_code

                Instantiate a local object instance of :py:mod:`Geo` with latitude and longitude as inputs (which
                automatically assigns them as attributes to the object). Then call the method on the object.

                .. code-block:: python

                    geo = api.geo(latitude=35.1, longitude=-106.7)
                    geo.get_elevation()

        .. container:: toggle

            .. container:: header

                **Example Response**

            .. container:: example_response

                The method returns a dictionary as shown in the example below, and assigns its contents as attributes
                to the local object instance of :py:mod:`Geo`.

                .. code-block:: python

                    {
                        "elevation": 1553.614
                    }

        :return: A dictionary with location information as shown in "Example Response".
        :rtype: dict
        """
        response = requests.get(
            url=self.api.base_url + "/Geo/{}/{}/Elevation".format(self.latitude, self.longitude),
            headers={"Authorization": "Bearer " + self.api.access_token}
        )
        attr = convert_json(response.json(), camel_to_snake)
        for key in attr:
            setattr(self, key, attr[key])

        return response

    def get_time_zone(self):
        """
        **GET** */Geo/* :py:attr:`latitude` */* :py:attr:`longitude` */TimeZone*

        Retrieves the time zone as a time shift in hours with respect to GMT for a given latitude and longitude. In
        addition to returning a dictionary with this information, the method also automatically assigns the  contents
        of the dictionary to the instance of :py:mod:`Geo` as attributes.

        .. container:: toggle

            .. container:: header

                **Required Attributes**

            .. container:: required_attributes

                .. csv-table:: Minimum required attributes on object to call this method successfully.
                    :delim: ;
                    :header: Field, Type, Description
                    :stub-columns: 1

                    latitude; float; North-South GPS coordinate. Must be between :py:data:`-90` and :py:data:`90` - units :py:data:`[decimal degrees]`.
                    longitude; float; East-West GPS coordinate Must be between :py:data:`-180` and :py:data:`180` units :py:data:`[decimal degrees]`.

        .. container:: toggle

            .. container:: header

                **Example Code**

            .. container:: example_code

                Instantiate a local object instance of :py:mod:`Geo` with latitude and longitude as inputs (which
                automatically assigns them as attributes to the object). Then call the method on the object.

                .. code-block:: python

                    geo = api.geo(latitude=35.1, longitude=-106.7)
                    geo.get_time_zone()

        .. container:: toggle

            .. container:: header

                **Example Response**

            .. container:: example_response

                The method returns a dictionary as shown in the example below, and assigns its contents as attributes
                to the local object instance of :py:mod:`Geo`.

                .. code-block:: python

                    {
                        "time_zone": -7.0
                    }

        :return: A dictionary with location information as shown in "Example Response".
        :rtype: dict
        """
        response = requests.get(
            url=self.api.base_url + "/Geo/{}/{}/TimeZone".format(self.latitude, self.longitude),
            headers={"Authorization": "Bearer " + self.api.access_token}
        )
        attr = convert_json(response.json(), camel_to_snake)
        for key in attr:
            setattr(self, key, attr[key])

        return response

    def __init__(self, api, latitude=None, longitude=None):
        """
        Initializes a local object instance of :py:mod:`Geo`.

        :param api: :py:class:`~plantpredict.api.Api` object.
        :type api: object
        :param latitude: North-South GPS coordinate. Must be between :py:data:`-90` and :py:data:`90` - units :py:data:`[decimal degrees]`.
        :type latitude: float
        :param longitude: East-West GPS coordinate Must be between :py:data:`-180` and :py:data:`180` units :py:data:`[decimal degrees]`.
        :type longitude: float
        """
        self.api = api

        self.latitude = latitude
        self.longitude = longitude

        super(Geo, self).__init__()
