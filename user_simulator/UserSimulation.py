
import json
from datetime import datetime
import requests
import hashlib


class User:

    def __init__(self):
        self._latest_error = ''
        #self._UserApikey = Userkey
        self._base_url = 'https://fep34ikk65.execute-api.us-east-1.amazonaws.com/dev'
        self._headers = {'Content-Type': 'application/json'}
        self._otp = ''

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
        Concat_username = FirstName[0:3]+LastName[0:3]+"username"
        Concat_password = FirstName[0:3] + LastName[0:3] + "password"
        print(Concat_username)
        print(Concat_password)
        data = {
            "firstname": FirstName,
            "lastname": LastName,
            "password": Concat_password,
            "user_type": "Passenger",
            "username": Concat_username


        }
        print(f'{self._base_url}{path}')
        res = requests.post(f'{self._base_url}{path}', json.dumps(data), headers=self._headers)
        print(res.text)
        print(res.status_code)
        print(res.headers)
        print(res.content)
        print(res)
        if res == "<Response [400]>":
            print(f'response - {res}')
            return {res}
        else:
            print("Err")
        return None

    def passenger_login(self, user_id, Password):
        path = "/api/users/login"
        username_hash = hashlib.sha256(user_id.encode())
        password_hash = hashlib.sha256(Password.encode())
        print(str(username_hash))
        print(str(password_hash))
        data = {
            "password": str(password_hash),
            "user_type": "Passenger",
            "username": str(username_hash)

        }

        res = requests.post(f'{self._base_url}{path}', json.dumps(data), headers=self._headers)
        print(res.text)
        print(res.status_code)
        print(res.headers)
        print(res.content)
        if res.status_code == 200:
            print(f'response - {res.content}')
            return {res.content}
        else:
            print('Error while retrieving data')
        return None

    def get_lat_long(self, location):
        location = location.replace(" ", "+")
        url = "https://nominatim.openstreetmap.org/search?q="+location+"&format=json&polygon_geojson=1&addressdetails=1"
        response = requests.get(
            url)
        resp_json_payload = response.json()
        print(resp_json_payload)
        resp_json_payload = dict(resp_json_payload[0])
        print(resp_json_payload)
        latitude  = resp_json_payload['lat']
        longitude = resp_json_payload['lon']
        return{'latitude':latitude, 'longitude': longitude}

    def book_taxi(self, user_id, Origin, Destination, taxi_type):
        path = "/api/rides/getaride"
        origin_lat_lon = self.get_lat_long(Origin)
        destination_lat_lon = self.get_lat_long(Destination)
        data = {
            "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            "destLat": destination_lat_lon['latitude'],
            "destLng": destination_lat_lon['longitude'],
            "startLat": origin_lat_lon['latitude'],
            "startLng": origin_lat_lon['longitude'],
            "vehicle_type": taxi_type

        }
        r = requests.post(f'{self._base_url}{path}', json.dumps(data), headers=self._headers)
        print(f'response1 - {r.text}')
        if r.status_code == 200:
            print(f'response - {r.text}')
            return r.text
        else:
            print('Error while retrieving data')
        return r.text

    def book_taxi_confirm(self,  user_id, taxi_num, Origin, Destination, taxi_type,apiKey):
        path = "/api/rides/confirmride"
        origin_lat_lon = get_lat_long(Origin)
        destination_lat_lon = get_lat_long(Destination)
        data = {
            "apiKey": apiKey,
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

    def start_ride(self, user_id, OTP, taxi_num, Origin, Destination, taxi_type,apiKey):
        path = "/api/rides/updateride"
        data = {
            "userId": user_id,
            "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            "vehicle_num": taxi_num,
            "Destination": Destination,
            "taxi_type": taxi_type,
            "Origin": Origin,
            "OTP": hashlib.sha256(OTP.encode()),
            "apiKey": apiKey,
            "startTime": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            "updateType": "startTime"

        }
        res = requests.post(f'{self._base_url}{path}', json.dumps(data), headers=self._headers)
        if res.status_code == 200:
            print(f'Your ride started at  - {res.start_time}')
            return res.text
        else:
            print('Error while retrieving data')
        return None

    def end_ride(self, user_id, OTP, taxi_num, Origin, Destination, taxi_type, apiKey):
        path = "/api/rides/updateride"
        data = {
            "userId": user_id,
            "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            "vehicle_num": taxi_num,
            "Destination": Destination,
            "taxi_type": taxi_type,
            "Origin": Origin,
            "OTP": hashlib.sha256(OTP.encode()),
            "apiKey": apiKey,
            "startTime": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            "updateType": "endTime"

        }
        res = requests.post(f'{self._base_url}{path}', json.dumps(data), headers=self._headers)
        if res.status_code == 200:
            print(f'Your ride has ended  - {res.end_time}')
            return res.text
        else:
            print('Error while retrieving data')
        return None