###########################################################################################################
#This function captures all server actions for Passenger Simulation
###########################################################################################################
import hashlib
import json
from datetime import datetime

import requests
from geopy.distance import geodesic
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from geopy.geocoders import Nominatim
import math


class User:

    def __init__(self):
        self._latest_error = ''
        self._base_url = 'https://fep34ikk65.execute-api.us-east-1.amazonaws.com/dev'
        self._headers = {'Content-Type': 'application/json'}
        self._otp = ''
        self.GApiKey= 'AIzaSyBL7zpEUMf0oScoY9oBdH2KcRbpJMPzVgk'
    @property
    def latest_error(self):
        print(self._latest_error)

    @property
    def users(self):
        return self._User
    def OTP(self):
        return self._otp


    def passenger_signup(self,FirstName, LastName):
        path = "/api/users/newuser"
        Concat_username = (FirstName[0:3] + LastName[0:3] + "username").lower()
        Concat_password = (FirstName[0:3] + LastName[0:3] + "password").lower()

        data = {
            "firstname": FirstName,
            "lastname": LastName,
            "password": str(hashlib.sha256(Concat_password.encode("utf-8") ).hexdigest()),
            "user_type": "Passenger",
            "username": str(hashlib.sha256(Concat_username.encode("utf-8") ).hexdigest())


        }

        res = requests.post(f'{self._base_url}{path}', json.dumps(data), headers=self._headers)

        if res.status_code==200:

            return {"UserName":Concat_username,"Password":Concat_password}
        else:
            return "SignUp Failed"


    def passenger_login(self, user_id, Password):
        path = "/api/users/login"
        username_lower = user_id.lower()
        password_lower = Password.lower()

        data = {
            "username": str(hashlib.sha256( username_lower.encode("utf-8")).hexdigest()),
            "password": str(hashlib.sha256( password_lower.encode("utf-8")).hexdigest()),
            "user_type": "Passenger"


        }

        res = requests.post(f'{self._base_url}{path}', json.dumps(data), headers=self._headers)

        if res.status_code == 200:

            return res.text
        else:

            return None

    def get_lat_long(self, location):

       location = location.replace(" ", "+")
       url = "https://maps.googleapis.com/maps/api/geocode/json?address="+location+"&key="+self.GApiKey
       response = requests.get(
       url)
       #print(response.json())
       if response !="None":
            resp_json_payload = response.json()
            resp_json_payload = resp_json_payload['results']
            resp_json_payload = resp_json_payload[0]
            latitude  = resp_json_payload['geometry']['location']['lat']
            longitude = resp_json_payload['geometry']['location']['lng']


            return{'latitude':latitude, 'longitude': longitude}

    def get_location(self, concat_lat_lng):

        url = "https://maps.googleapis.com/maps/api/geocode/json?latlng="+concat_lat_lng+"&sensor=false&key="+self.GApiKey
        response = requests.get(
            url)
        if response != "None":
            resp_json_payload = response.json()

            resp_json_payload = resp_json_payload['results']
            resp_json_payload = resp_json_payload[0]

            address = resp_json_payload['formatted_address']

            return address

    def get_distance(self, to_lat_lng, frm_lat_lng):

            lat1 = frm_lat_lng['latitude']
            lon1 = frm_lat_lng['longitude']
            lat2 = to_lat_lng['latitude']
            lon2 = to_lat_lng['longitude']

            R = 6371000  # radius of Earth in meters
            phi_1 = math.radians(lat1)
            phi_2 = math.radians(lat2)

            delta_phi = math.radians(lat2 - lat1)
            delta_lambda = math.radians(lon2 - lon1)

            a = math.sin(delta_phi / 2.0) ** 2 + \
                math.cos(phi_1) * math.cos(phi_2) * \
                math.sin(delta_lambda / 2.0) ** 2
            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

            meters = R * c  # output distance in meters
            distance = meters / 1000.0  # output distance in kilometers

            return distance

    def get_ride_details(self, ApiKey, Booked_time):
        try:
            path = "/api/rides/getridedetails"
            data= {
                "apiKey": ApiKey,
                "booked_time": Booked_time,


            }

            r = requests.post(f'{self._base_url}{path}', json.dumps(data), headers=self._headers)

            if r.status_code == 200:
                return r.json()
            else:
                print(r.text)
                return None
        except TypeError:
            return None

    def book_taxi(self, user_id, Origin, Destination, taxi_type):#this will block the taxi temporarily so that other users cannot book the taxi before current user confirms or denies the taxi
        try:
            path = "/api/rides/getaride"
            origin_lat_lon = self.get_lat_long(Origin)
            destination_lat_lon = self.get_lat_long(Destination)

            data = {

                "dest_lat": destination_lat_lon['latitude'],
                "dest_lng": destination_lat_lon['longitude'],
                "start_lat": origin_lat_lon['latitude'],
                "start_lng": origin_lat_lon['longitude'],
                "vehicle_type": taxi_type

            }

            r = requests.post(f'{self._base_url}{path}', json.dumps(data), headers=self._headers)

            if r.status_code == 200:
                return r.json()
            else:
                print(r.text)
                return None
        except TypeError:
            return None
    def book_taxi_confirm(self,  user_id, taxi_num, Origin, Destination, taxi_type, apiKey):#this will confirm the taxi and taxi starts moving towards the passenger
        path = "/api/rides/confirmride"
        origin_lat_lon = self.get_lat_long(Origin)
        destination_lat_lon = self.get_lat_long(Destination)
        booked_time = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        data = {
            "apiKey": apiKey,
            "booked_time": booked_time,
            "dest_address": Destination,
            "dest_lat": destination_lat_lon['latitude'],
            "dest_lng": destination_lat_lon['longitude'],
            "start_address": Origin,
            "start_lat": origin_lat_lon['latitude'],
            "start_lng": origin_lat_lon['longitude'],
            "vehicle_num": taxi_num,
            "scheduled_time": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            "vehicle_type": taxi_type

        }
        res = requests.post(f'{self._base_url}{path}', json.dumps(data), headers=self._headers)
        #print(res.json())
        if res.status_code == 200:

            return res.text,booked_time
        else:

            return None
    def get_taxi_curr_location(self,  to_location,OTP,taxi_num):
        path = "/api/rides/getridelocation"
        to_loc_lat_lon = self.get_lat_long(to_location)
        data = {
                "otpHash": str(hashlib.sha256( OTP.encode("utf-8") ).hexdigest()),
                "vehicle_num": taxi_num

        }
        res = requests.post(f'{self._base_url}{path}', json.dumps(data), headers=self._headers)
        if res.status_code == 200:
            resp_json_payload = res.json()

            lat_lng = resp_json_payload['current_vehicle_location']['coordinates']
            concat_lat_lng = ','.join([str(lat_lng[0]), str(lat_lng[1])])
            driver_address = self.get_location(concat_lat_lng)
            lat_lng= {'latitude':lat_lng[0], 'longitude': lat_lng[1]}
            distance = self.get_distance(to_loc_lat_lon,lat_lng)

            
            return driver_address,distance
        else:
            return None


    def start_ride(self, OTP, taxi_num, Origin, Destination,  apiKey):
        path = "/api/rides/updateride"
        origin_lat_lon = self.get_lat_long(Origin)
        destination_lat_lon = self.get_lat_long(Destination)
        data = {
            "OTPHash": str(hashlib.sha256(OTP.encode("utf-8")).hexdigest()),
            "apiKey": apiKey,
            "dest_lat": destination_lat_lon['latitude'],
            "dest_lng": destination_lat_lon['longitude'],
            "start_lat": origin_lat_lon['latitude'],
            "start_lng": origin_lat_lon['longitude'],
            "start_time": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            "update_type": "startTime",
            "vehicle_num": taxi_num

        }
        res = requests.post(f'{self._base_url}{path}', json.dumps(data), headers=self._headers)
        if res.status_code == 200:
            return res.text
        else:
            return None


    def end_ride(self,  OTP, taxi_num, apiKey):
        path = "/api/rides/updateride"
        data = {

            "OTPHash": str(hashlib.sha256( OTP.encode("utf-8") ).hexdigest()),
            "apiKey": apiKey,
            "end_time": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            "update_type": "endTime",
            "vehicle_num": taxi_num

        }
        res = requests.post(f'{self._base_url}{path}', json.dumps(data), headers=self._headers)
        if res.status_code == 200:

            return res.text
        else:
            return None


    def feedback(self,  OTP, apiKey, comments, rating):
        path = "/api/rides/updateride"
        data = {
            "OTPHash": str(hashlib.sha256( OTP.encode("utf-8") ).hexdigest()),
            "apiKey": apiKey,
            "passenger_comments": comments,
            "passenger_rating": rating,
            "update_type": "feedback"

        }
        res = requests.post(f'{self._base_url}{path}', json.dumps(data), headers=self._headers)
        if res.status_code == 200:

            return res
        else:
            return None
