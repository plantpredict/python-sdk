import json
import requests

from plantpredict.utilities import convert_json, camel_to_snake, snake_to_camel, decorate_all_methods
from plantpredict.error_handlers import handle_refused_connection, handle_error_response, APIError


@decorate_all_methods(handle_refused_connection)
@decorate_all_methods(handle_error_response)
class PlantPredictEntity(object):
    def create(self, *args):
        """Generic POST request."""
        response = requests.post(
            url=self.api.base_url + self.create_url_suffix,
            headers={"Authorization": "Bearer " + self.api.access_token},
            json=convert_json(self.__dict__, snake_to_camel)
        )

        # power plant is the exception that doesn't have its own id. has a project and prediction id
        try:
            self.id = response.json()['id'] if 200 <= response.status_code < 300 else None
        except ValueError:
            pass

        return response

    def delete(self):
        """Generic DELETE request."""

        return requests.delete(
            url=self.api.base_url + self.delete_url_suffix,
            headers={"Authorization": "Bearer " + self.api.access_token}
        )

    def get(self):
        """Generic GET request."""
        response = requests.get(
            url=self.api.base_url + self.get_url_suffix,
            headers={"Authorization": "Bearer " + self.api.access_token}
        )
        if response.status_code == 404:
            raise APIError(response.status_code, response.content, response.url)
        else:
            attr = convert_json(response.json(), camel_to_snake)
        for key in attr:
            setattr(self, key, attr[key])

        return response

    def update(self):
        """Generic PUT request."""

        return requests.put(
            url=self.api.base_url + self.update_url_suffix,
            headers={"Authorization": "Bearer " + self.api.access_token},
            json=convert_json(self.__dict__, snake_to_camel)
        )

    def __init__(self, api, **kwargs):
        self.api = api

        self.create_url_suffix = None
        self.delete_url_suffix = None
        self.get_url_suffix = None
        self.update_url_suffix = None

        self.__dict__.update(kwargs)
