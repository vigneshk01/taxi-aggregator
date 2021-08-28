import datetime
from datetime import timedelta

from bson.json_util import dumps
from flask import Flask, request

from database import Database

app = Flask(__name__)
db = Database()
# TAXI_COLLECTION = 'taxi-reg-data'
TAXI_COLLECTION = 'taxi'
LOCATION_COLLECTION = 'boundary'
RIDE_DETAILS_COLLECTION = 'ridedetails'
STREAM_COLLECTION = 'taxi-location-stream'
SPECIAL_EVENTS_COLLECTION = 'special_events'
USERS_COLLECTION = 'users'


@app.route("/", methods=['GET'])
def home():
    return "welcome home"


@app.route("/taxi", methods=['GET'])
def get_taxi_list():
    taxi_data = db.get_all_data(TAXI_COLLECTION, {}, {'_id': 0})
    list_cur = list(taxi_data)
    json_data = dumps(list_cur)
    return json_data


@app.route("/taxi/shiftCheck", methods=['GET'])
def shift_checker():
    shift_start = db.get_all_data(TAXI_COLLECTION, {'Shift_Start_Time': "06:00"}, {'_id': 0})
    shift_end = db.get_all_data(TAXI_COLLECTION, {'shift_end_time': "18:00"}, {'_id': 0})
    return


@app.route("/taxi/specialEvent", methods=['GET'])
def get_special_events():
    timestamp = datetime.datetime.now()
    curr_date = str(timestamp.date() + timedelta(days=-1))
    end_date = str(timestamp.date())

    curr_time = str(timestamp.time())
    end_time = str((timestamp + timedelta(minutes=60)).time())

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


@app.route("/bookTaxi", methods=['GET'])
def book_taxi():
    return


@app.route("/bookTaxi/{ID}", methods=['GET'])
def confirm_taxi():
    return


if __name__ == "__main__":
    app.run(debug=True)
