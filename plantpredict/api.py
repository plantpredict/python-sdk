import requests
import json

from plantpredict.project import Project
from plantpredict.prediction import Prediction
from plantpredict.powerplant import PowerPlant
from plantpredict.geo import Geo
from plantpredict.inverter import Inverter
from plantpredict.module import Module
from plantpredict.weather import Weather
from plantpredict.ashrae import ASHRAE


class Api(object):

    def __get_access_token(self):
        """
        """
        response = requests.post(
            url=self.__okta_auth_url,
            headers={"content-type": "application/x-www-form-urlencoded"},
            params={
                "grant_type": "password",
                "scope": "openid offline_access",
                "username": self.username,
                "password": self.password,
                "client_id": self.client_id,
                "client_secret": self.client_secret
            }
        )

        # set authentication token as global variable
        try:
            self.access_token = json.loads(response.content)['access_token']
            self.refresh_token = json.loads(response.content)['refresh_token']
        except KeyError:
            pass

        return response

    def refresh_access_token(self):
        response = requests.post(
            url=self.__okta_auth_url,
            headers={"content-type": "application/x-www-form-urlencoded"},
            params={
                "refresh_token": self.refresh_token,
                "grant_type": "refresh_token",
                "scope": "offline_access",
                "client_id": self.client_id,
                "client_secret": self.client_secret
            }
        )

        # set authentication token as global variable
        try:
            self.access_token = json.loads(response.content)['access_token']
            self.refresh_token = json.loads(response.content)['refresh_token']
        except KeyError:
            pass

        return response

    def __init__(self, username, password, client_id, client_secret, base_url="https://api.plantpredict.com",
                 okta_auth_url="https://afse.okta.com/oauth2/aus3jzhulkrINTdnc356/v1/token"):
        self.base_url = base_url
        self.__okta_auth_url = okta_auth_url

        self.username = username
        self.password = password
        self.client_id = client_id
        self.client_secret = client_secret

        self.access_token = None
        self.refresh_token = None

        self.__get_access_token()

        super(Api, self).__init__()

    def project(self, **kwargs):
        return Project(self, **kwargs)

    def prediction(self, **kwargs):
        return Prediction(self, **kwargs)

    def powerplant(self, **kwargs):
        return PowerPlant(self, **kwargs)

    def geo(self, **kwargs):
        return Geo(self, **kwargs)

    def inverter(self, **kwargs):
        return Inverter(self, **kwargs)

    def module(self, **kwargs):
        return Module(self, **kwargs)

    def weather(self, **kwargs):
        return Weather(self, **kwargs)

    def ashrae(self, **kwargs):
        return ASHRAE(self, **kwargs)
