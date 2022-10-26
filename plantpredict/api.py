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
            url=self.auth_url,
            headers={"content-type": "application/x-www-form-urlencoded"},
            params={
                "grant_type": "client_credentials",
                "scope": "transactions/post transactions/get",
                "client_id": self.client_id,
                "client_secret": self.client_secret
            }
        )

        # set authentication token as global variable
        try:
            self.access_token = response.json()['access_token']
        except KeyError:
            print("Authentification failed. Response:", response.text)
            pass

        return response

    def __init__(self, client_id, client_secret, base_url="https://api.plantpredict.terabase.energy",
                 auth_url="https://terabase-prd.auth.us-west-2.amazoncognito.com/oauth2/token"):
        self.base_url = base_url
        self.auth_url = auth_url

        self.client_id = client_id
        self.client_secret = client_secret

        self.access_token = None

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
