import datetime
from datetime import timedelta
from json import dumps

from app.database import Database

# BASE = "http://127.0.0.1:5000/"
#
# response = requests.get(BASE + "taxi")
# print(response.json())
db = Database()
SPECIAL_EVENTS_COLLECTION = 'special_events'

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
