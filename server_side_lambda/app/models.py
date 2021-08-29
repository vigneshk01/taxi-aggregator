import datetime
from json import dumps
import random

from bson.son import SON
from flask import Flask, request

from server_side_lambda.app.database import Database

app = Flask(__name__)
db = Database()
# TAXI_COLLECTION = 'taxi-reg-data'
TAXI_COLLECTION = 'taxi'
LOCATION_COLLECTION = 'boundary'
RIDE_DETAILS_COLLECTION = 'ridedetails'
STREAM_COLLECTION = 'taxi_location_stream'
SPECIAL_EVENTS_COLLECTION = 'special_events'
USERS_COLLECTION = 'users'
BOOKING_HISTORY_COLLECTION = 'booking_request_history'


@app.route("/", methods=['GET'])
def home():
    return "welcome home"


@app.route("/taxi", methods=['GET'])
def get_taxi_list():  # will get called every minute
    timestamp = datetime.datetime.now()
    curr_time = timestamp.time().strftime("%H:%M")
    end_time = (timestamp + datetime.timedelta(minutes=1)).strftime("%H:%M")
    taxi_data = db.get_all_data(TAXI_COLLECTION, {'Shift_Start_Time': {'$gte': curr_time, '$lt': end_time}},
                                {'_id': 0, 'TaxiID': 1})
    list_cur = list(taxi_data)
    json_data = dumps(list_cur)
    return json_data


@app.route("/taxi/specialEvent", methods=['GET'])
def get_special_events():
    timestamp = datetime.datetime.now()
    curr_date = str(timestamp.date())
    end_date = str(timestamp.date() + datetime.timedelta(days=+1))

    curr_time = str(timestamp.time())
    end_time = str((timestamp + datetime.timedelta(minutes=60)).time())

    events_data = db.get_all_data(SPECIAL_EVENTS_COLLECTION,
                                  {'date': {'$gte': curr_date, '$lt': end_date},
                                   '$or': [
                                       {'start_time': {'$gte': curr_time, '$lt': end_time}},
                                       {'end_time': {'$gte': curr_time, '$lt': end_time}}
                                   ]
                                   }, {'_id': 0})

    list_cur = list(events_data)
    json_data = dumps(list_cur)
    return json_data


@app.route("/locations", methods=['GET'])
def get_stationing_points():
    location_data = db.get_all_data(LOCATION_COLLECTION, {'geometry.type': 'Point'}, {'_id': 0})
    list_cur = list(location_data)
    json_data = dumps(list_cur)
    return json_data


@app.route("/stream", methods=['POST'])
def stream_locations():
    if request.method == 'POST':
        location_data = db.insert_single_data(STREAM_COLLECTION, request.json)
        return str(location_data)


@app.route("/newRequests", methods=['GET'])
def get_new_ride_requests():
    return


@app.route("/taxi/migrate", methods=['GET'])
def migrate_taxi():
    return


@app.route("/bookTaxi", methods=['POST'])
def book_taxi():
    data = request.json
    location = data['current_location']
    range_query = {'current_location': SON([("$near", location), ("$maxDistance", 1000)])}
    coll_documents = db.get_all_data(STREAM_COLLECTION, range_query, {'_id': 0, 'current_location': 1, 'taxiID': 1,
                                                                      'taxi_type': 1})
    list_coll = list(coll_documents)
    if len(list_coll) > 0:
        json_data = dumps(list_coll)
        data['msg'] = 'cabs_available'
        db.insert_single_data(BOOKING_HISTORY_COLLECTION, data)
        return json_data
    else:
        data['msg'] = 'no_nearby_cabs'
        db.insert_single_data(BOOKING_HISTORY_COLLECTION, data)
        return None


@app.route("/bookTaxi/confirm", methods=['POST'])
def confirm_taxi():
    if request.method == 'POST':
        data = request.json
        print(data["source_location"])
        confirmation_id = random.randint(1000, 9999)
        param = {
            "user_ID": data['user_ID'],
            "Taxi_ID": data['taxi_ID'],
            "booking_time": datetime.datetime.now(),
            "booking_confirmation_ID": confirmation_id,
            "source": data['source'],
            "destination": data['destination'],
            "source_location": data["source_location"],
            "destination_location": data["dest_location"],
            "request_status": "open"
        }
        db.insert_single_data(RIDE_DETAILS_COLLECTION, param)
        return str(confirmation_id)

    """ query = {
        "user_ID": "user_02",
        "Taxi_ID": "taxi_02",
        "booking_time": "19:00:00",
        "booking_confirmation_ID": "2356",
        "trip_start_time": "19:00:00",
        "trip_end_ime": "22:00:00",
        "source": "Madiwala",
        "Destination": "Sarjapur",
        "source_location": {
            "type": "Point",
            "coordinates": [12.8747, 77.6582]
        },
        "dest_location": {
            "type": "Point",
            "coordinates": [12.8610, 77.7837]
        },
        "request_status": "fulfilled"
    }
"""

    return None


if __name__ == "__main__":
    app.run(debug=True)
