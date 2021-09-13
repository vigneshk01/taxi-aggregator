import datetime
import random
from json import dumps
from bson.son import SON
from flask import Flask, request, make_response, jsonify
from app.database import Database
from sklearn.cluster import KMeans
import config

app = Flask(__name__)
app.config.from_object(config)
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


@app.route("/taxi/<shift_id>", methods=['GET'])
def get_taxi_list(shift_id):  # will get called every minute
    curr_time = datetime.now().time()
    if(curr_time.hour > 5 and curr_time.hour < 18):
        curr_time = '06:00'
    else:
        curr_time = '18:00'
    taxi_data = db.get_all_data(TAXI_COLLECTION, {'Shift_Start_Time': curr_time},
                                {'_id': 0, 'TaxiID': 1, 'taxi_type': 1})
    list_cur = list(taxi_data)
    json_data = dumps(list_cur)
    return json_data
    '''
    if int(shift_id) == 6:
        print(shift_id)
        curr_time = "06:00"
        taxi_data = db.get_all_data(app.config["TAXI_COLLECTION"], {'Shift_Start_Time': curr_time},
                                    {'_id': 0, 'TaxiID': 1, 'taxi_type': 1})
        list_cur = list(taxi_data)
        json_data = dumps(list_cur)
        return json_data
    '''


# @app.route("/taxi/18", methods=['GET'])
# def get_taxi_list():  # will get called every minute
#     timestamp = datetime.datetime.now()
#     curr_time = timestamp.time().strftime("%H:%M")
#     end_time = (timestamp + datetime.timedelta(minutes=1)).strftime("%H:%M")
#     taxi_data = db.get_all_data(TAXI_COLLECTION, {'Shift_Start_Time': {'$gte': curr_time, '$lt': end_time}},
#                                 {'_id': 0, 'TaxiID': 1})
#     list_cur = list(taxi_data)
#     json_data = dumps(list_cur)
#     return json_data


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


@app.route("/boundary", methods=['GET'])
def get_boundary():
    location_data = db.get_all_data(app.config["LOCATION_COLLECTION"], {'geometry.type': 'Polygon'}, {'_id': 0})
    list_cur = list(location_data)
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
    data = request.json
    lattitude = request.args.get('lat')
    longitude = request.args.get('long')
    #coll_documents = db.get_single_data(STREAM_COLLECTION, data, {'_id': 0, 'current_location': 1, 'taxiID': 1,
    #                                                              'taxi_type': 1})
    query = {"request_status": "open", 'taxiID': request.args.get('taxi_ID')}

    coll_documents = db.get_single_data(RIDE_DETAILS_COLLECTION, query, {'_id': 0, 'current_location': 1, 'taxiID': 1,
                                                                  'taxi_type': 1})
    json_data = dumps(coll_documents)
    return json_data


@app.route("/taxi/migrate", methods=['GET'])
def migrate_taxi():
    time_frame = datetime.datetime.now() - datetime.timedelta(minutes = 20)
    query = {'timestamp': {'$gte': time_frame}}
    coll_documents = db.get_all_data(BOOKING_HISTORY_COLLECTION, query, {'_id': 0, 'current_location': 1})
    list_coll = list(c['current_location']['coordinates'] for c in coll_documents)
    kmeans = KMeans(init = "random", n_clusters = 5, n_init = 5, max_iter = 100)
    kmeans.fit(list_coll)
    #print(kmeans.cluster_centers_)
    json_list = []
    for cc in kmeans.cluster_centers_:
        json_list.append({
            'current_location': {
                'type': 'Point',
                'coordinates': [cc[0], cc[1]]
            }
        })
    json_obj = dumps(json_list)
    return json_obj


@app.route("/bookTaxi", methods=['POST'])
def book_taxi():
    data = request.json
    location = data['current_location']
    taxi_type = data['preffered_taxi_type']
    if taxi_type == 'All':
        agg_query = [
            {
                '$geoNear'  : {
                    'near': location,
                    'distanceField': 'distance', 
                    'maxDistance': 1000,
                }
            },{
                '$match'    : {
                    'status': 'Available'
                }
            }, {
                '$sort'     : {
                    'taxiID': 1, 
                    'timestamp': -1
                }
            }, {
                '$group'    : {
                    '_id': '$taxiID',
                    'taxiID': {'$first': '$taxiID'},
                    'current_location': {'$first': '$current_location'}, 
                    'taxi_type': {'$first': '$taxi_type'}
                }       
            }
        ]
        # $group is not updating properly. Other pipes are working correctly.
    else:
        agg_query = [
            {
                '$geoNear'  : {
                    'near': location,
                    'distanceField': 'distance', 
                    'maxDistance': 1000,
                }
            },{
                '$match'    : {
                    'status': 'Available',
                    'taxi_type': taxi_type
                }
            }, {
                '$sort'     : {
                    'taxiID': 1, 
                    'timestamp': -1
                }
            }, {
                '$group'    : {
                    '_id': '$taxiID',
                    'taxiID': {'$first': '$taxiID'},
                    'current_location': {'$first': '$current_location'}, 
                    'taxi_type': {'$first': '$taxi_type'}
                }       
            }
        ]
    #coll_documents = db.get_all_data(STREAM_COLLECTION, range_query, {'_id': 0, 'current_location': 1, 'taxiID': 1,
    #                                                                  'taxi_type': 1})
    coll_documents = db.generate_aggregate(STREAM_COLLECTION, agg_query)
    #Get list of n nearest taxis 
    data['timestamp'] = datetime.datetime.now()
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


@app.errorhandler(404)
def resource_not_found(e):
    return make_response(jsonify(error='Not found!'), 404)
# if __name__ == "__main__":
#     app.run(debug=True)
