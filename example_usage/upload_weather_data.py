import json
import plantpredict
from plantpredict.enumerations import WeatherDataProviderEnum, LibraryStatusEnum, WeatherDataTypeEnum, \
    WeatherPLevelEnum
import numpy as np


# authenticate using API credentials
api = plantpredict.Api(
    username="insert username here",
    password="insert password here",
    client_id="insert client_id here",
    client_secret="insert client_secret here"
)

# load JSON file containing weather time series
with open('weather_details.json', 'rb') as json_file:
    weather_details = json.load(json_file)

# get location info from latitude and longitude
latitude = 35.0
longitude = -119.0
geo = api.geo(latitude=latitude, longitude=longitude)
location_info = geo.get_location_info()

# initial the weather file and populate REQUIRED weather fields
weather = api.weather()
weather.name = "Python SDK Test Weather"
weather.latitude = 35.0
weather.longitude = -119.0
weather.country = location_info['country']
weather.country_code = location_info['country_code']
weather.data_provider = WeatherDataProviderEnum.METEONORM
weather.weather_details = weather_details

# populate additional weather metadata
weather.elevation = round(geo.get_elevation()["elevation"], 2)
weather.locality = location_info['locality']
weather.region = location_info['region']
weather.state_province = location_info['state_province']
weather.state_province_code = location_info['state_province_code']
weather.time_zone = geo.get_time_zone()['time_zone']
weather.status = LibraryStatusEnum.DRAFT_PRIVATE
weather.data_type = WeatherDataTypeEnum.MEASURED
weather.p_level = WeatherPLevelEnum.P95
weather.time_interval = 60  # minutes
weather.global_horizontal_irradiance_sum = round(
    sum([w['global_horizontal_irradiance'] for w in weather_details])/1000, 2
)
weather.diffuse_horizontal_irradiance_sum = round(
    sum([w['diffuse_horizontal_irradiance'] for w in weather_details])/1000, 2
)
weather.direct_normal_irradiance_sum = round(
    sum([w['direct_normal_irradiance'] for w in weather_details])/1000, 2
)
weather.average_air_temperature = np.round(np.mean([w['temperature'] for w in weather_details]), 2)
weather.average_relative_humidity = np.round(np.mean([w['relative_humidity'] for w in weather_details]), 2)
weather.average_wind_speed = np.round(np.mean([w['windspeed'] for w in weather_details]), 2)
weather.max_air_temperature = np.round(max([w['temperature'] for w in weather_details]), 2)

# create weather file in PlantPredict
weather.create()
