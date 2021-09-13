import random
#import numpy as np
import json
#import boto3
#import math
#from api import Api
from datetime import datetime
#from shapely.geometry import Point
#from shapely.geometry.polygon import Polygon
import requests


class User:
    base_url = 'https://fep34ikk65.execute-api.us-east-1.amazonaws.com/dev'
    def __init__(self):
        self._latest_error = ''
        self._User = []
        self._base_url = self.base_url
        self._headers = {'Content-type': 'application/json'}
        self._otp = ''

    @property
    def latest_error(self):
        print(self._latest_error)

    @property
    def users(self):
        return self._User
    def OTP(self):
        return self._otp

    def get_lat_long(self, location):
        location = location.replace(" ", "+")
        url = "https://nominatim.openstreetmap.org/search?q="+location+"&format=json&polygon_geojson=1&addressdetails=1"
        response = requests.get(
            url)
        resp_json_payload = response.json()
        resp_json_payload = dict(resp_json_payload[0])
        print(resp_json_payload)
        latitude  = resp_json_payload['lat']
        longitude = resp_json_payload['lon']
        return{'latitude':latitude, 'longitude': longitude}

    def book_taxi(self, user_id, Origin, Destination, taxi_type):
        path =  "/api/rides/getaride"
        origin_lat_lon = get_lat_long(Origin)
        destination_lat_lon = get_lat_long(Destination)
        data = {
            "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            "destLat": destination_lat_lon['latitude'],
            "destLng": destination_lat_lon['longitude'],
            "startLat": origin_lat_lon['latitude'],
            "startLng": origin_lat_lon['longitude'],
            "vehicle_type": taxi_type

        }
        r = requests.post(f'{self._base_url}{path}', json.dumps(data), headers=self._headers)
        if r.status_code == 200:
            print(f'response - {r.text}')
            return r.text
        else:
            print('Error while retrieving data')
        return None

    def book_taxi_confirm(self,  user_id, taxi_num, Origin, Destination, taxi_type):
        path = "/api/rides/confirmride"
        origin_lat_lon = get_lat_long(Origin)
        destination_lat_lon = get_lat_long(Destination)
        data = {
            "apiKey": "3b8987fc336962d247878853df95d8f615dd99bc16b65d320fd8a2cc0b3ea8cd",
            "bookedTime": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            "destAddress": Destination,
            "destLat": destination_lat_lon['latitude'],
            "destLng": destination_lat_lon['longitude'],
            "startAddress": Origin,
            "startLat": origin_lat_lon['latitude'],
            "startLng": origin_lat_lon['longitude'],
            "vehicleNum": taxi_num,
            "vehicle_type": taxi_type

        }
        res = requests.post(f'{self._base_url}{path}', json.dumps(data), headers=self._headers)
        if res.status_code == 200:
            print(f'response - {res.text}')
            return res.text
        else:
            print('Error while retrieving data')
        return None

    def start_ride(self, user_id, taxi_num, Origin, Destination, taxi_type):
        path = "/api/rides/updateride"
        data = {
            "userId": user_id,
            "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            "vehicle_num": taxi_num,
            "Destination": Destination,
            "taxi_type": taxi_type,
            "Origin": Origin,

            "OTP": "52fd190882ff5bd2c24a93f6a8b28767328474d6e95c2257279d079225e81ebe",
            "apiKey": "3b8987fc336962d247878853df95d8f615dd99bc16b65d320fd8a2cc0b3ea8cd",
            "startTime": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            "updateType": "startTime"

        }
        res = requests.post(f'{self._base_url}{path}', json.dumps(data), headers=self._headers)
        if res.status_code == 200:
            print(f'response - {res.text}')
            return res.text
        else:
            print('Error while retrieving data')
        return None