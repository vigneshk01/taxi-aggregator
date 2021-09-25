# Imports APi class from the project to provide basic functionality for database
import random
import numpy as np
import json
import boto3
import math
from api import Api
import time
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon


class Taxi:

    def __init__(self):
        self._api = Api()
        self._latest_error = ''
        self._Taxi = []

    # Latest error is used to store the error string in case an issue.
    @property
    def latest_error(self):
        return self._latest_error

    @property
    def taxis(self):
        return self._Taxi

    def get_taxis(self):
        taxi_list = self._api.get_request('taxi/6')
        self._Taxi = taxi_list

    # Template for data to push 
    def taxi_template(self, api_key, vehicle_num, status, random_location):
        template_dict = {
            "user_type": 'Taxi',
            "update_type": 'taxiLoc',
            "apiKey": api_key,
            "vehicle_num": vehicle_num,
            "status": status,
            "lng": random_location[0],
            "lat": random_location[1]
        }
        return template_dict


class KinesisPublishAndMovement(Taxi):
    BASED_FILE_LOCATION = 'Movement_Location_History_Json'

    def __init__(self):
        Taxi.__init__(self)
        self._Data_Stream_Name = 'taxi-movement'
        self._Kinesis_Handle = boto3.client('kinesis', region_name="us-east-1")
        self._recent_locations = dict()

    def publish_kinesis_data(self, data):
        message = json.dumps(data)
        response = self._Kinesis_Handle.put_record(
            StreamName=self._Data_Stream_Name, Data=message, PartitionKey=data['vehicle_num']
        )
        print(f'Data pushed successfully and res- {response}')

    def get_recent_long_lat_for_taxi_id(self):
        long_lat_data = []
        if self._recent_locations:
            long_lat_data = [self._recent_locations['lng'], self._recent_locations['lat']]
        else:
            print('No location history found')
        return long_lat_data

    def get_taxi_data(self):
        return self._recent_locations

    # function will calculate and generate new lat and long based on old lat long
    def calculate_movement(self, long, lat, distance=0.3):
        R = 6378.1  # Radius of the Earth
        brng = 1.57  # Bearing is 90 degrees converted to radians.
        d = distance  # Distance in km

        lon1 = math.radians(long)  # Current long point converted to radians
        lat1 = math.radians(lat)  # Current lat point converted to radians

        lat2 = math.asin(math.sin(lat1) * math.cos(d / R) +
                         math.cos(lat1) * math.sin(d / R) * math.cos(brng))

        lon2 = lon1 + math.atan2(math.sin(brng) * math.sin(d / R) * math.cos(lat1),
                                 math.cos(d / R) - math.sin(lat1) * math.sin(lat2))

        lon2 = math.degrees(lon2)
        lat2 = math.degrees(lat2)

        return [lon2, lat2]

    def read_recent_location(self, taxi_id):
        recent_loc_file = open(f'{self.BASED_FILE_LOCATION}/{taxi_id}_location_history.json', "r")
        self._recent_locations = json.load(recent_loc_file)
        recent_loc_file.close()

    def update_location_to_json(self, taxi_id, taxi_data):
        recent_loc_file = open(f'{self.BASED_FILE_LOCATION}/{taxi_id}_location_history.json', "w")
        json.dump(taxi_data, recent_loc_file, indent=4)
        recent_loc_file.close()

    def choose_random_from_list(self, locality_location):
        return random.choice(locality_location)

    def check_point_in_boundary(self, long, lat, boundary):
        # This is where boundary is in list of list structure
        boundary_list = [tuple(x) for x in boundary[0]]
        point = Point(long, lat)
        # This will check point in boundary or not
        polygon = Polygon(boundary_list)
        return polygon.contains(point)

    def stream_template_data(self, taxi, long, lat):
        new_long_lat = [long, lat]
        status = taxi['status']
        if int(time.time()) % 7 == 0:
            status = "INACTIVE"
        stream_template = Taxi.taxi_template(
            self, taxi['APIKey'], taxi['vehicle_num'], status, new_long_lat
        )
        # print(stream_template)
        # For Api stream insert
        # self._api.post_stream('/api/users/updateuser', stream_template)
        # For Direct kinesis insert
        self.publish_kinesis_data(stream_template)
        return stream_template


class RandomTaxiGenerateModel(KinesisPublishAndMovement):
    BASED_FILE_LOCATION = 'Movement_Location_History_Json'
    LOCATION = 'location_in_boundary/location.json'

    def __init__(self):
        KinesisPublishAndMovement.__init__(self)
        self._api = Api()
        self._latest_error = ''
        self._boundary = []
        self._location_list = []

    # Latest error is used to store the error string in case an issue.
    @property
    def latest_error(self):
        return self._latest_error

    @property
    def location_list(self):
        return self._location_list

    def extract_location(self):
        if len(self._boundary) != 0:
            return self._boundary['geometry']['coordinates']
        else:
            print('No location found')
            return []

    def get_boundary(self):
        boundary = self._api.get_request('/api/ridesearch/getboundary')
        if len(boundary) == 0:
            print('Sorry no boundary found')
            self._latest_error = 'Sorry no boundary found'
        else:
            self._boundary = boundary

    def show_boundary_location(self):
        boundary_location = self.extract_location()
        print(boundary_location)

    # This function is used to generate sample of given number from given boundary coordinates
    def generate_random_lat_long_sample(self, min_value, max_value, sample):
        random_sample = list(np.random.uniform(min_value, max_value, sample))
        print(random_sample)

    # Used for generation of single random by giving lat/long coordinates
    def generate_random_lat_long_value(self, min_value, max_value):
        randomvalue = random.uniform(min_value, max_value)
        print(randomvalue)

    def get_data_random_location(self):
        get_all_location = open(self.LOCATION, "r")
        location_list = json.load(get_all_location)
        self._location_list = location_list
        get_all_location.close()

    def generate_random_from_list(self):
        return random.choice(self._location_list)

    def create_json_with_taxi_id(self, taxi_id, taxi_data):
        filename = f'{self.BASED_FILE_LOCATION}/{taxi_id}_location_history.json'
        with open(filename, 'w') as file_object:  # open the file in write mode
            json.dump(taxi_data, file_object, indent=4)

    def generate_random_location_for_taxi(self, taxis, index):
        if len(taxis) == 0:
            print('No Taxis is register in the system')
        else:
            for taxi in taxis:
                if index > len(self._location_list):
                    random_location = self.generate_random_from_list()
                else:
                    random_location = self._location_list[index]
                taxi_dict = Taxi.taxi_template(
                    self, taxi['APIKey'], taxi['vehicle_num'], taxi['status'], random_location
                )
                # print(taxi_dict)
                # For Direct kinesis insert
                KinesisPublishAndMovement.publish_kinesis_data(self, taxi_dict)
                # For Api stream insert
                # self._api.post_stream('/api/users/updateuser', taxi_dict)
                self.create_json_with_taxi_id(taxi['vehicle_num'], taxi_dict)
