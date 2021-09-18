
import json
from datetime import datetime
import requests
import hashlib
from geopy.distance import geodesic

class User:

    def __init__(self):
        self._latest_error = ''
        #self._UserApikey = Userkey
        self._base_url = 'https://fep34ikk65.execute-api.us-east-1.amazonaws.com/dev'
        self._headers = {'Content-Type': 'application/json'}
        self._otp = ''
        self.GApiKey= 'AIzaSyDyRi7MuGjrLBWt32v_T1U4DEeTAjdjnr8'
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
        Concat_username = FirstName[0:3]+LastName[0:3] + "username"
        Concat_password = FirstName[0:3] + LastName[0:3] + "password"
        print(Concat_username)
        print(Concat_password)
        data = {
            "firstname": FirstName,
            "lastname": LastName,
            "password": str(hashlib.sha256(Concat_username.encode("utf-8") ).hexdigest()),
            "user_type": "Passenger",
            "username": str(hashlib.sha256(Concat_password.encode("utf-8") ).hexdigest())


        }
        print(f'{self._base_url}{path}')
        res = requests.post(f'{self._base_url}{path}', json.dumps(data), headers=self._headers)
        print(res.text)
        print(res.status_code)
        print(res.headers)
        print(res.content)
        print(res)
        if res.status_code==200:

            return "SignUp Successful"
        else:
            return "SignUp Failed"


    def passenger_login(self, user_id, Password):
        path = "/api/users/login"
        username_hash = hashlib.sha256( user_id.encode("utf-8") ).hexdigest()
        password_hash = hashlib.sha256( Password.encode("utf-8") ).hexdigest()
        print(str(username_hash))
        print(str(password_hash))
        data = {
            "username": str(username_hash),
            "password": str(password_hash),
            "user_type": "Passenger"


        }

        res = requests.post(f'{self._base_url}{path}', json.dumps(data), headers=self._headers)
        print(res.text)
        print(res.status_code)
        print(res.headers)
        print(res.content)
        if res.status_code == 200:
            print(f'response - {res.text}')
            return res.text
        else:
            print('Error while retrieving data')
        return None

    def get_lat_long(self, location):
        location = location.replace(" ", "+")
        url = "https://maps.googleapis.com/maps/api/geocode/json?address="+location+"&key="+self.GApiKey
        response = requests.get(
            url)
        resp_json_payload = response.json()
        print(resp_json_payload)
        resp_json_payload = resp_json_payload['results']
        resp_json_payload = resp_json_payload[0]
        print(resp_json_payload)
        latitude  = resp_json_payload['geometry']['location']['lat']
        longitude = resp_json_payload['geometry']['location']['lng']
        return{'latitude':latitude, 'longitude': longitude}

    def get_location(self, latitude, longitude):
        concat_lat_lng = ','.join([str(latitude) ,str(longitude)])
        url = "https://maps.googleapis.com/maps/api/geocode/json?latlng="+concat_lat_lng+"&sensor=false&key="+self.GApiKey
        response = requests.get(
            url)
        resp_json_payload = response.json()
        print(resp_json_payload)
        resp_json_payload = resp_json_payload['results']
        resp_json_payload = resp_json_payload[0]
        print(resp_json_payload)
        address = resp_json_payload['formatted_address']
        return address
    def get_distance(self, to_lat_lng, frm_lat_lng):

        print(to_lat_lng, frm_lat_lng)
        distance = geodesic((to_lat_lng['latitude'],to_lat_lng['longitude']), (frm_lat_lng['latitude'],frm_lat_lng['longitude'])).km
        print(distance)
        return distance

    def book_taxi(self, user_id, Origin, Destination, taxi_type):
        path = "/api/rides/getaride"
        origin_lat_lon = self.get_lat_long(Origin)
        destination_lat_lon = self.get_lat_long(Destination)
        data = {
            #"timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            "dest_lat": destination_lat_lon['latitude'],
            "dest_lng": destination_lat_lon['longitude'],
            "start_lat": origin_lat_lon['latitude'],
            "start_lng": origin_lat_lon['longitude'],
            "vehicle_type": taxi_type

        }
        r = requests.post(f'{self._base_url}{path}', json.dumps(data), headers=self._headers)
        print(r.status_code)
        if r.status_code == 200:
            return r.text
        else:
            print('Error while retrieving data')
        return None

    def book_taxi_confirm(self,  user_id, taxi_num, Origin, Destination, taxi_type,apiKey):
        path = "/api/rides/confirmride"
        origin_lat_lon = self.get_lat_long(Origin)
        destination_lat_lon = self.get_lat_long(Destination)
        data = {
            "apiKey": apiKey,
            "booked_time": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
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
        if res.status_code == 200:
            print(f'response - {res.text}')

            return res.text
        else:
            print('Error while retrieving data')
        return None
    def get_taxi_curr_location(self,  to_location,OTP,taxi_num):
        path = "/api/rides/getridelocation"
        tp_loc_lat_lon = self.get_lat_long(to_location)
        data = {
            "otpHash": str(hashlib.sha256( OTP.encode("utf-8") ).hexdigest()),
            "vehicle_num": taxi_num

        }
        res = requests.post(f'{self._base_url}{path}', json.dumps(data), headers=self._headers)
        if res.status_code == 200:
            print(f'response - {res.text}')
            print(res.text)
            resp_json_payload = json.loads(res.text)
            print(resp_json_payload['current_vehicle_location']['coordinates'])
            lat_lng = resp_json_payload ['current_vehicle_location']['coordinates']
            driver_address = self.get_location(lat_lng[0],lat_lng[1])
            print(lat_lng)
            print(tp_loc_lat_lon )
            lat_lng= {'latitude':lat_lng[0], 'longitude': lat_lng[1]}
            distance = self.get_distance(tp_loc_lat_lon,lat_lng)
            return driver_address,distance
        else:
            print('Error while retrieving data')
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
            print(f'Your ride started at  - {res.text}')
            return res.text
        else:
            print(f'Error while retrieving data{res.text}')
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
            "OTP": str(hashlib.sha256( OTP.encode("utf-8") ).hexdigest()),
            "apiKey": apiKey,
            "startTime": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            "updateType": "endTime"

        }
        res = requests.post(f'{self._base_url}{path}', json.dumps(data), headers=self._headers)
        if res.status_code == 200:
            print(f'Your ride has ended  - {res.end_time}')
            return res.end_time
        else:
            print('Error while retrieving data')
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
            print('Error while retrieving data')
        return None