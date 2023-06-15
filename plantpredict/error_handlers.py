from __future__ import print_function
import time
import requests
import json

from plantpredict.utilities import convert_json, camel_to_snake


def handle_refused_connection(function):
    def function_wrapper(*args, **kwargs):
        connection_error = True
        while connection_error:
            try:
                connection_error = False
                return function(*args, **kwargs)
            except requests.exceptions.ConnectionError:
                print("Connection refused, trying again...")
                time.sleep(7)
    function_wrapper.__name__ = function.__name__
    function_wrapper.__doc__ = function.__doc__
    return function_wrapper


def handle_error_response(function):
    def function_wrapper(*args, **kwargs):
        response = function(*args, **kwargs)
        try:
            # if the authorization is invalid, refresh the API access token
            if response.status_code == 401:
                args[0].api.__get_access_token()

            # if there is a sever side error, return the error message
            elif not 200 <= response.status_code < 300:
                raise APIError(response.status_code, response.content, response.url)

            # if the HTTP request receives a successful response
            else:

                # if the response contains content, return it
                if response.content:
                    if "Queue" in response.url:
                        return response.json()

                    else:
                        # if it is a list, use convert_json method in list comprehension
                        if isinstance(response.json(), list):
                            return [convert_json(i, camel_to_snake) for i in response.json()]
                        else:
                            return convert_json(response.json(), camel_to_snake)

                # if the response does not contain content, return a generic success message
                else:
                    return {'is_successful': True}

        except AttributeError:
            return response

    function_wrapper.__name__ = function.__name__
    function_wrapper.__doc__ = function.__doc__
    return function_wrapper


class APIError(Exception):

    def __init__(self, status, errors, url):
        self.status = status
        self.errors = errors
        self.url = url

    def __str__(self):
        return "HTTP Status Code {}: {} at URL {}".format(
            self.status,
            self.errors,
            self.url
        )
