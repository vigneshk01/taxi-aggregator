# Imports MongoClient for base level access to the local MongoDB
from pymongo import MongoClient


class Database:
    # Class static variables used for database host ip and port information, database name
    # Static variables are referred to by using <class_name>.<variable_name>
    HOST = '127.0.0.1'
    PORT = '27017'
    # DB_NAME = 'test'
    DB_NAME = 'glcapstone_taxi_db'
    CONNECTION_STRING = "mongodb+srv://<>/test" \
                        "?retryWrites=true&w=majority"

    def __init__(self):
        self._db_conn = MongoClient(f'mongodb://{Database.HOST}:{Database.PORT}')
        #self._db_conn = MongoClient(Database.CONNECTION_STRING)
        self._db = self._db_conn[Database.DB_NAME]

    # This method finds a single document using field information provided in the key parameter
    # It assumes that the key returns a unique document. It returns None if no document is found
    def get_single_data(self, collection, key, *args):
        db_collection = self._db[collection]
        document = db_collection.find_one(key, *args)
        return document

    # This method inserts the data in a new document. It assumes that any uniqueness check is done by the caller
    def insert_single_data(self, collection, data):
        db_collection = self._db[collection]
        document = db_collection.insert_one(data)
        return document.inserted_id

    def create_index_on_coll(self, collection, data, unique_flag=False):
        db_collection = self._db[collection]
        index_obj = db_collection.create_index(data, unique=unique_flag)
        return index_obj

    def generate_aggregate(self, collection, data):
        db_collection = self._db[collection]
        document = db_collection.aggregate(data)
        return document

    def get_all_data(self, collection, key, *args):
        db_collection = self._db[collection]
        document = db_collection.find(key, *args)
        return document
