# Imports Database class from the project to provide basic functionality for database access
import random
import numpy as np
import json
import boto3
import math
from api import Api
from datetime import datetime
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

    def taxi_template(self, taxi_id, coordinates, taxi_type, taxi_status='Available'):
        template_dict = {
            "taxiId": taxi_id,
            "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            "status": taxi_status,
            "taxi_type": taxi_type,
            "current_location": {
                "type": "Point",
                "coordinates": coordinates
            }
        }
        return template_dict


class KinesisPublishAndMovement(Taxi):
    LOCATION_FILE = 'Movement_Location_History_Json/taxi_location_history.json'

    def __init__(self):
        Taxi.__init__(self)
        self._Data_Stream_Name = 'taxi-movement'
        self._Kinesis_Handle = boto3.client('kinesis', region_name="us-east-1")
        self._recent_locations = dict()

    def publish_kinesis_data(self, data):
        message = json.dumps(data)
        response = self._Kinesis_Handle.put_record(
            StreamName=self._Data_Stream_Name, Data=message, PartitionKey=data['taxiId']
        )
        print(f'Data pushed successfully and res- {response}')

    def get_recent_long_lat_by_taxi_id(self, taxi_id):
        long_lat_data = []
        if self._recent_locations:
            long_lat_data = self._recent_locations[taxi_id]['current_location']['coordinates']
        else:
            print('No location history found')
        return long_lat_data

    def get_taxi_data(self, taxi_id):
        return self._recent_locations[taxi_id]

    def calculate_movement(self, long, lat, distance=0.2):
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

    def read_recent_location(self):
        recent_loc_file = open(self.LOCATION_FILE, "r")
        self._recent_locations = json.load(recent_loc_file)
        recent_loc_file.close()

    def update_location(self, taxi_id, data):
        self._recent_locations[taxi_id] = data

    def update_all_location_to_json(self):
        recent_loc_file = open(self.LOCATION_FILE, "w")
        json.dump(self._recent_locations, recent_loc_file, indent=4)
        recent_loc_file.close()

    def choose_random_from_list(self, locality_location):
        return random.choice(locality_location)

    def check_point_in_boundary(self, long, lat, boundary):
        # This is where boundary is in list of list structure
        boundary_list = [tuple(x) for x in boundary[0]]
        point = Point(long, lat)
        polygon = Polygon(boundary_list)
        return polygon.contains(point)

    def stream_template_data(self, taxi_id, long, lat, taxi_type):
        new_long_lat = [long, lat]
        stream_template = Taxi.taxi_template(self, taxi_id, new_long_lat, taxi_type)
        print(f'Pushed Data - {stream_template}')
        # For Api stream insert
        #self._api.post_stream('/stream', stream_template)
        # For Direct kinesis insert
        #self.publish_kinesis_data(stream_template)
        return stream_template


class RandomTaxiGenerateModel(KinesisPublishAndMovement):

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
            return self._boundary[0]['geometry']['coordinates']
        else:
            print('No location found')
            return []

    def get_boundary(self):
        boundary = self._api.get_request('boundary')
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
        get_all_location = self._api.get_request('locations')
        location_list = [all_loc['geometry']['coordinates'] for all_loc in get_all_location]
        self._location_list = location_list

    def generate_random_from_list(self):
        return random.choice(self._location_list)

    def generate_random_location_for_taxi(self, taxis):
        list_of_taxi_dict = dict()

        if len(taxis) == 0:
            print('No Taxis is register in the system')
        else:
            for taxi in taxis:
                random_location = self.generate_random_from_list()
                taxi_dict = Taxi.taxi_template(self, taxi['TaxiID'], random_location, taxi['taxi_type'])
                # For Direct kinesis insert
                #KinesisPublishAndMovement.publish_kinesis_data(self, taxi_dict)
                # For Api stream insert
                #self._api.post_stream('/stream', taxi_dict)
                list_of_taxi_dict[taxi['TaxiID']] = taxi_dict

            filename = 'Movement_Location_History_Json/taxi_location_history.json'
            with open(filename, 'w') as file_object:  # open the file in write mode
                json.dump(list_of_taxi_dict, file_object, indent=4)
