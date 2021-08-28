import json
import os
import base64
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure


def connect_db(connection_string, db_name):
    db_conn = MongoClient(connection_string)
    db_instance = None
    try:
        db_instance = db_conn[db_name]
    except ConnectionFailure:
        print('Connection error to connect mongoDb')

    return db_instance


def insert_data(db, collection, data):
    db_collection = db[collection]
    document = db_collection.insert_one(data)
    return document.inserted_id

def lambda_handler(event, context):
    db = connect_db(os.environ['CONNECTIONSTRING'], os.environ['DB_NAME'])
    insert_ids = []
    for record in event['Records']:
        # Kinesis data is base64 encoded so decode here
        payload = base64.b64decode(record["kinesis"]["data"])
        payload_dict = json.loads(payload.decode('utf-8'))
        print("Message arrived: " + str(payload_dict))
        insert_id = insert_data(db, 'taxi-location-stream', payload_dict)
        print(f'Data inserted succesfully in DB with Id - {insert_id}')
        insert_ids.append(insert_id)

    return {
        'statusCode': 200,
        'body': 'success'
    }