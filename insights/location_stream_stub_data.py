import datetime
import random
import string
import time
import json
import geojson
import haversine
import openrouteservice
import pandas as pd
from bson import ObjectId
from shapely.geometry import Point, Polygon
from database import Database

RIDE_COLLECTION = 'rides'
LOCATION_STREAM_COLLECTION = 'location_stream'

if __name__ == "__main__":
    db = Database()
    ride_collection = []
    query = {}
    coll_data = db.get_all_data(RIDE_COLLECTION, query)
    ride_collection = list(coll_data)
    df = pd.DataFrame(ride_collection)
    df['passenger_id'] = list(str(y) for y in df['passenger_id'])
    df['_id'] = list(str(y) for y in df['_id'])
    x = df['start_loc']
    df['src_coordinates'] = [[y['coordinates'][1], y['coordinates'][0]] for y in x]
    df[['src_cord_x', 'src_cord_y']] = df['src_coordinates'].apply(pd.Series)
    x = df['dest_loc']
    df['dest_coordinates'] = [[y['coordinates'][1], y['coordinates'][0]] for y in x]
    df[['dest_cord_x', 'dest_cord_y']] = df['dest_coordinates'].apply(pd.Series)
    client = openrouteservice.Client(base_url='http://localhost:8080/ors')
    for row in df.iterrows():
        src_x, src_y = row[1]['src_coordinates']
        dest_x, dest_y  = row[1]['dest_coordinates']
        coords = ((src_x, src_y), (dest_x, dest_y))
        route = client.directions(coords)['routes'][0]['geometry']
        decoded = openrouteservice.convert.decode_polyline(route)
        d_start = datetime.datetime.strptime(row[1]['start_time'], '%Y-%m-%dT%H:%M:%S.%f')
        d_end = datetime.datetime.strptime(row[1]['end_time'], '%Y-%m-%dT%H:%M:%S.%f')
        # delta = d_end - d_start
        # delta = int(delta.total_seconds() / len(decoded['coordinates']))
        # i = 0
        # for point in decoded['coordinates']:
        #     data = {
        #         'ride_id': row[1]['_id'],
        #         'start_loc': row[1]['start_loc'],
        #         'dest_loc': row[1]['dest_loc'],
        #         'current_loc': {"type": "Point", "coordinates": [point[1], point[0]]},
        #         'start_time': row[1]['start_time'], 
        #         'current_time': datetime.datetime.strftime(d_start + datetime.timedelta(seconds = (i * delta)), '%Y-%m-%dT%H:%M:%S.%f')[:-3],
        #         'vehicle_num': row[1]['vehicle_num']
        #     }
        #     db.insert_single_data(LOCATION_STREAM_COLLECTION, data)
        #     i += 1
        data = {
            'ride_id': row[1]['_id'],
            'start_loc': row[1]['start_loc'],
            'dest_loc': row[1]['dest_loc'],
            'current_loc': decoded,
            'start_time': row[1]['start_time'], 
            'vehicle_num': row[1]['vehicle_num']
        }
        db.insert_single_data(LOCATION_STREAM_COLLECTION, data)