import requests

from plantpredict.plant_predict_entity import PlantPredictEntity
from plantpredict.error_handlers import handle_refused_connection, handle_error_response
from plantpredict.enumerations import EntityTypeEnum


class Inverter(PlantPredictEntity):
    """
    """
    def create(self):
        """POST /Inverter"""
        self.create_url_suffix = "/Inverter"
        return super(Inverter, self).create()

    def delete(self):
        """DELETE /Inverter/{Id}"""
        self.delete_url_suffix = "/Inverter/{}".format(self.id)
        return super(Inverter, self).delete()

    def get(self):
        """GET /Inverter/{Id}"""
        self.get_url_suffix = "/Inverter/{}".format(self.id)
        return super(Inverter, self).get()

    def update(self):
        """PUT /Inverter"""
        self.update_url_suffix = "/Inverter".format(self.id)
        return super(Inverter, self).update()

    @handle_refused_connection
    @handle_error_response
    def change_status(self, new_status, note=""):
        """

        :param new_status:
        :param note:
        :return:
        """
        return requests.post(
            url=self.api.base_url + "/Inverter/Status",
            headers={"Authorization": "Bearer " + self.api.access_token},
            json=[{
                "name": self.name,
                "id": self.id,
                "type": EntityTypeEnum.INVERTER,
                "status": new_status,
                "note": note
            }]
        )

    @handle_refused_connection
    @handle_error_response
    def get_kva(self, elevation, temperature, use_cooling_temp):
        """
        Uses the given elevation and temperature to interpolate a kVa rating from the inverter's kVa curves.

        :param float elevation: Elevation at which to evaluate the inverter kVa rating - units :py:data:`[m]`.
        :param float temperature: Temperature at which to evaluate the inverter kVa rating - units :py:data:`[deg-C]`.
        :param bool use_cooling_temp: Determines if the calculation should use the plant design cooling temperature (
                                      at 99.6 degrees).
        :return: # TODO after new API response is implemented
        """
        return requests.get(
            url=self.api.base_url + "/Inverter/{}/kVa".format(self.id),
            headers={"Authorization": "Bearer " + self.api.access_token},
            params={"elevation": elevation, "temperature": temperature, "useCoolingTemp": use_cooling_temp}
        )

    @handle_refused_connection
    @handle_error_response
    def get_inverter_list(self):
        """
        :return: a list of all inverter to which a user has access.
        """
        return requests.get(
            url=self.api.base_url + "/Inverter",
            headers={"Authorization": "Bearer " + self.api.access_token},
           )
