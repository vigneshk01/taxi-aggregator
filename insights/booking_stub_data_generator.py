import datetime
import random
import json
import haversine
import openrouteservice

from bson import ObjectId
from shapely.geometry import Point, Polygon
from database import Database
from rides_stub_data_generator import MyRide

RIDE_COLLECTION = 'rides'
BOOKING_COLLECTION = 'booking'
LOCATION_STREAM_COLLECTION = 'location_stream'

# Set to 1 to generate location data
GENERATE_LOCATION_DATA = 1

# DAILY_PASSENGER_COUNT is used twice a day to generate rush hour,
# i.e atleast 20 ride requests will be made during rush hour
DAILY_PASSENGER_COUNT = 20
# RANDOM_PASSENGER_COUNT is used for the amount of users availabe to make ride requests above the DAILY_PASSENGER_COUNT
# The generator works on randomness, a random value will be seleted from 1 to RANDOM_PASSENGER_COUNT/2 every hour 
# to get the hourly ride count
RANDOM_PASSENGER_COUNT = 50
# TAXI_COUNT is the total number of available taxis
TAXI_COUNT = 50

# The generator will generate rides and bookings from SHIFT_START till SHIFT_END
SHIFT_START = 6
SHIFT_END = 18
# RUSH_HOUR_1 is used to indicate the 1st rush hour of the day
# It will happen RUSH_HOUR_1 hours after SHIFT_START, i.e 6 + 3 = 9
RUSH_HOUR_1 = 3
# RUSH_HOUR_2 is used to indicate the 2nd rush hour of the day
# It will happen RUSH_HOUR_2 hours after SHIFT_START, i.e 6 + 8 = 14
RUSH_HOUR_2 = 8

# The amount of bookings that fail because no taxis were avalaible.
# This value is read as 1 in FAILED_BOOKING_PROB will be a failed booking
# The generator works on randomness so with more bookings the probability will be seen
FAILED_BOOKING_PROB = 10
# The amount of spam bookings the user tries to make every 10 seconds after a failed booking
# The reties has no chance of becoming a successful booking
# This value is read as 1 in SPAM_BOOKING_PROB of a failed booking will be a spam booking
# The generator works on randomness so with more bookings the probability will be seen
SPAM_BOOKING_PROB = 10
# The max amount of reties the user tries to make a spam booking 
# The generator works on randomness so with more bookings the probability will be seen
MAX_SPAM_COUNT = 5

# Starting date of the data. In the format: dd-mm-yyyy
START_DATE = "01-08-2021"
# Number of days of data to be generated
DAYS_TO_RUN = 31
# Format used in storing datetime in the database
TIME_FORMAT = '%Y-%m-%dT%H:%M:%S'

# The probabilities of a booking a ride from it's corresponding LAT_LONG
# a number is randomly generated from 1 to HIGH_PROB + MID_PROB + LOW_PROB + RANDOM_PROB
# LOW_PROB is selected if the number is less than LOW_PROB
# MID_PROB is selected if the number is less than LOW_PROB + MID_PROB
# HIGH_PROB is selected if the number is less than LOW_PROB + MID_PROB + HIGH_PROB
# A random location within BANGALORE_POLYGON is selected if the number is greater than LOW_PROB + MID_PROB + HIGH_PROB
# The LAT_LONG from the corressponding list(HIGH, MID, LOW) is selected in random
HIGH_PROB_SRC = 9
MID_PROB_SRC = 2
LOW_PROB_SRC = 1
RANDOM_PROB_SRC = 8
LOW_LAT_LONG_SRC = [(12.9035, 77.4914), (12.8546, 77.5676)]
MID_LAT_LONG_SRC = [(12.9872, 77.5197), (13.1002, 77.5995), (13.0276, 77.6339)]
HIGH_LAT_LONG_SRC = [(12.9976, 77.6129), (12.9212, 77.6203), (12.9619, 77.5990)]
HIGH_PROB_DEST = 9
MID_PROB_DEST = 2
LOW_PROB_DEST = 1
RANDOM_PROB_DEST = 8
LOW_LAT_LONG_DEST = [(12.9035, 77.4914), (12.8546, 77.5676)]
MID_LAT_LONG_DEST = [(12.9872, 77.5197), (13.1002, 77.5995), (13.0276, 77.6339)]
HIGH_LAT_LONG_DEST = [(12.9976, 77.6129), (12.9212, 77.6203), (12.9619, 77.5990)]

# On day START_DATE + SPECIAL_DAY, 
# at SHIFT_START + SPECIAL_HOUR_1, SPECIAL_BOOKING_COUNT bookings at this hour will have there destination location SPECIAL_LAT_LONG
# at SHIFT_START + SPECIAL_HOUR_2, SPECIAL_BOOKING_COUNT bookings at this hour will have there source location SPECIAL_LAT_LONG
SPECIAL_LAT_LONG = (12.9564, 77.7005)
SPECIAL_DAY = 7
SPECIAL_HOUR_1 = 0  # Start Time  
SPECIAL_HOUR_2 = 11 # End Time
SPECIAL_BOOKING_COUNT = 20

BANGALORE_BOUNDARY_JSON = 'db_structure_and_data/map_data/bengaluru_simple_polygon.geojson.json'
with open(BANGALORE_BOUNDARY_JSON) as f:
    data = json.load(f)
BANGALORE_POLYGON_DATA = data['features'][0]['geometry']
BANGALORE_POLYGON = Polygon([tuple(l) for l in BANGALORE_POLYGON_DATA['coordinates'][0]])

passenger_rating_lst = ["1:Poor Ride", "2:Below Average Ride", "3:Decent Ride", "4:Good Ride", "5:Awesome Ride"]
taxi_types = ["UTILITY", "DELUXE", "LUXURY"]
types_cost = [10, 15, 25]

class Bookings(MyRide):
    def __init__(self):
        self.daily_passenger_list = self.generate_passenger_data(DAILY_PASSENGER_COUNT)
        self.random_passenger_list_odd = self.generate_passenger_data(int(RANDOM_PASSENGER_COUNT / 2))
        self.random_passenger_list_even = self.generate_passenger_data(int(RANDOM_PASSENGER_COUNT / 2))
        self.vehicle_list = self.generate_vehicle_details(TAXI_COUNT)
        self.used_vehicle = dict.fromkeys(self.vehicle_list, 0)
        self.ride_collection = []
        self._db = Database()

    def generate_passenger_data(self, count = 20):
        pl = []
        for i in range(count):
            passenger =  ObjectId()
            pl.append(passenger)
        return pl

    def get_rides(self):
        query = {}
        aggr = {'_id': 0}
        coll_data = self._db.get_all_data(RIDE_COLLECTION, query, aggr)
        self.ride_collection = list(c['passenger_id']['start_loc']['dest_loc']['booked_time']['vehicle_type'] for c in coll_data)

    def get_location_details(self):
        x = random.randint(1, HIGH_PROB_SRC + MID_PROB_SRC + LOW_PROB_SRC + RANDOM_PROB_SRC)
        y = random.randint(1, HIGH_PROB_DEST + MID_PROB_DEST + LOW_PROB_DEST + RANDOM_PROB_DEST)
        if x < HIGH_PROB_SRC:
            s = random.choice(HIGH_LAT_LONG_SRC)
        elif x < HIGH_PROB_SRC + MID_PROB_SRC:
            s = random.choice(MID_LAT_LONG_SRC)
        elif x < HIGH_PROB_SRC + MID_PROB_SRC + LOW_PROB_SRC:
            s = random.choice(LOW_LAT_LONG_SRC)
        else:
            s = generate_random()
        if y < HIGH_PROB_DEST:
            d = random.choice(HIGH_LAT_LONG_DEST)
        elif y < HIGH_PROB_DEST + MID_PROB_DEST:
            d = random.choice(MID_LAT_LONG_DEST)
        elif y < HIGH_PROB_DEST + MID_PROB_DEST + LOW_PROB_DEST:
            d = random.choice(LOW_LAT_LONG_DEST)
        else:
            d = generate_random()
        source = (s[0] + (random.randrange(10, 99) / 10000),  s[1] + (random.randrange(10, 99) / 10000))
        dest = (d[0] + (random.randrange(10, 99) / 10000), d[1] + (random.randrange(10, 99) / 10000))
        lat_long = [source, dest]
        return lat_long

    def get_distance(self, source, dest):
        dist = haversine.haversine(source, dest)
        return dist
    
    def get_cost(self, dist, taxi_type):
        if taxi_type == taxi_types[0]:
            return dist * types_cost[0]
        elif taxi_type == taxi_types[1]:
            return dist * types_cost[1]
        elif taxi_type == taxi_types[2]:
            return dist * types_cost[2]
    
    def add_time(self, vehicle, minutes):
        hour = int(minutes / 60)
        self.used_vehicle[vehicle] = hour

def rearrange(l):
    # starting sorted array:
    # 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11
    # swaps the sorted array to get it in the following:
    # 0, 2, 4, 10, 8, 6, 7, 9, 11, 5, 3, 1
    # This is used to simulate hourly request count in the following order:
    #   incresing count from index 0 to 3
    #   Peak count at index 3
    #   decreasing but still a high count from index 3 to 5
    #   increasing count from index 5 to 8
    #   Peak count at index 8
    #   decreasing count from index 8 to 11
    l.sort()
    l[1], l[2] = l[2], l[1]
    l[3], l[10] = l[10], l[3]
    l[4], l[8] = l[8], l[4]
    l[5], l[6] = l[6], l[5]
    l[7], l[9] = l[9], l[7]
    l[2], l[8] = l[8], l[2]
    l[6], l[9] = l[9], l[6]
    l[11], l[8] = l[8], l[11]

def generate_random():
    minx, miny, maxx, maxy = BANGALORE_POLYGON.bounds
    check = 0
    while check == 0:
        pnt = Point(random.uniform(minx, maxx), random.uniform(miny, maxy))
        if BANGALORE_POLYGON.contains(pnt):
            check = 1
            return (pnt.y, pnt.x)
    return (pnt.y, pnt.x)

if __name__ == "__main__":
    book = Bookings()
    start = datetime.datetime.strptime(START_DATE, "%d-%m-%Y")  # default "01-08-2021"

    if GENERATE_LOCATION_DATA:
        client = openrouteservice.Client(base_url='http://localhost:8080/ors')

    for day in range(DAYS_TO_RUN):
        date = start + datetime.timedelta(days = day)
        hourly_ride_count = list(random.randint(0, RANDOM_PASSENGER_COUNT / 2) for i in range(SHIFT_END - SHIFT_START))
        rearrange(hourly_ride_count)

        if day == SPECIAL_DAY:
            hourly_ride_count[SPECIAL_HOUR_1] = hourly_ride_count[SPECIAL_HOUR_1] + SPECIAL_BOOKING_COUNT
            hourly_ride_count[SPECIAL_HOUR_2] = hourly_ride_count[SPECIAL_HOUR_2] + SPECIAL_BOOKING_COUNT

        for hour in range(SHIFT_START, SHIFT_END):
            # at start of hour decrement each hour of used taxi
            useable_vehicle = []
            for i in book.used_vehicle:
                if book.used_vehicle[i] > 0:
                    book.used_vehicle[i] = book.used_vehicle[i] - 1
                if book.used_vehicle[i] == 0:
                    useable_vehicle.append(i)

            if hour % 2 == 0:
                user_list = random.sample(book.random_passenger_list_even, hourly_ride_count[hour - SHIFT_START])
            else:
                user_list = random.sample(book.random_passenger_list_odd, hourly_ride_count[hour - SHIFT_START])

            if hour == SHIFT_START + RUSH_HOUR_1 or hour == SHIFT_START + RUSH_HOUR_2:
                user_list.extend(book.daily_passenger_list)

            special_trip_start_count = 0
            special_trip_end_count = 0

            for user in user_list:
                vehicle_type = book.get_vehicle_type()

                gen_time = book.get_time_details(date, hour)
                timestamp = gen_time["booked_time"]
                
                lat_long = book.get_location_details()
                if day == SPECIAL_DAY and hour == SPECIAL_HOUR_1 and special_trip_start_count < SPECIAL_BOOKING_COUNT:
                    lat_long[1] = SPECIAL_LAT_LONG
                    lat_long[1] = (lat_long[1][0] + (random.randrange(10, 99) / 10000), lat_long[1][1] + (random.randrange(10, 99) / 10000))
                    special_trip_start_count += 1
                if day == SPECIAL_DAY and hour == SPECIAL_HOUR_2 and special_trip_end_count < SPECIAL_BOOKING_COUNT:
                    lat_long[0] = SPECIAL_LAT_LONG
                    lat_long[0] = (lat_long[0][0] + (random.randrange(10, 99) / 10000), lat_long[0][1] + (random.randrange(10, 99) / 10000))
                    special_trip_end_count += 1

                book_query = {
                    'passenger_id': user,
                    'start_loc': {'type': "Point", "coordinates": lat_long[0]},
                    'dest_loc': {"type": "Point", "coordinates": lat_long[1]},
                    'vehicle_type': vehicle_type,
                    'booked_time' : datetime.datetime.strftime(timestamp, TIME_FORMAT+'.%f')[:-3]
                }

                # spam booking 1/10 of a failed booking
                # failed booking 1/10 of a booking
                check_failed = random.randint(1, FAILED_BOOKING_PROB)
                if check_failed == 1:
                    book_query['server_message'] = 'no cabs available' 
                    check_spam = random.randint(1, SPAM_BOOKING_PROB)
                    if check_spam == 1:
                        spam_count = random.randint(1, MAX_SPAM_COUNT)
                        for i in range(spam_count - 1):
                            #print(book_query)
                            book.insert_data_to_db(BOOKING_COLLECTION, book_query)
                            timestamp = timestamp + datetime.timedelta(seconds = 10)
                            del book_query['_id']
                            book_query['booked_time'] = datetime.datetime.strftime(timestamp, TIME_FORMAT+'.%f')[:-3]

                elif len(useable_vehicle) == 0:
                    book_query['server_message'] = 'no cabs available' 

                else:
                    vehicle = random.choice(useable_vehicle)
                    vehicle_num = vehicle.split(':')[0]
                    vehicle_type = vehicle.split(':')[1]

                    resp = book.get_passenger_ratings()
                    rating = resp["rating"]
                    comment = resp["comment"]

                    dist = book.get_distance(lat_long[0], lat_long[1])
                    cost = book.get_cost(dist, vehicle_type)

                    book_query['vehicle_type'] = vehicle_type
                    book_query['server_message'] = 'success'

                    delta = gen_time["end_time"] - gen_time["start_time"]
                    book.add_time(vehicle, int(delta.total_seconds() / 60))
                    useable_vehicle.remove(vehicle)

                    ride_query = {
                        'passenger_id': user,
                        'start_loc': {'type': "Point", "coordinates": lat_long[0]},
                        'dest_loc': {"type": "Point", "coordinates":  lat_long[1]}, 
                        'booked_time': datetime.datetime.strftime(gen_time["booked_time"], TIME_FORMAT+'.%f')[:-3],
                        'start_time': datetime.datetime.strftime(gen_time["start_time"], TIME_FORMAT+'.%f')[:-3], 
                        'end_time': datetime.datetime.strftime(gen_time["end_time"], TIME_FORMAT+'.%f')[:-3], 
                        'vehicle_type': vehicle_type,
                        'vehicle_num': vehicle_num, 
                        'cost': cost, 
                        'passenger_rating': rating,
                        'passenger_comments': comment,
                        'total_distance': dist
                    }
                    # print(ride_query)
                    book.insert_data_to_db(RIDE_COLLECTION, ride_query)

                    if GENERATE_LOCATION_DATA:
                        src_x, src_y = lat_long[0][1], lat_long[0][0]
                        dest_x, dest_y  = lat_long[1][1], lat_long[1][0]
                        coords = ((src_x, src_y), (dest_x, dest_y))
                        route = client.directions(coords)['routes'][0]['geometry']
                        decoded = openrouteservice.convert.decode_polyline(route)
                        location_query = {
                            'ride_id': str(ride_query['_id']),
                            'start_loc': ride_query['start_loc'],
                            'dest_loc': ride_query['dest_loc'],
                            'current_loc': decoded,
                            'start_time': ride_query['start_time'], 
                            'vehicle_num': ride_query['vehicle_num']
                        }
                        # print(location_query)
                        book.insert_data_to_db(LOCATION_STREAM_COLLECTION, location_query)
    
                # print(book_query)
                book.insert_data_to_db(BOOKING_COLLECTION, book_query)