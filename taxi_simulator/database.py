from pymongo import MongoClient


class Database:
    HOST = '127.0.0.1'
    PORT = '27017'
    CONNECTIONSTRING = 'ENTER CONNECTION STRING HERE'
    DB_NAME = 'glcapstone_taxi_db'

    def __init__(self):
        self._db_conn = MongoClient(Database.CONNECTIONSTRING)
        self._db = self._db_conn[Database.DB_NAME]

    # This method inserts the data in a new document.
    def insert_single_data(self, collection, data):
        db_collection = self._db[collection]
        document = db_collection.insert_one(data)
        return document.inserted_id

    def get_boundary(self, collection, query):
        db_collection = self._db[collection]
        document = db_collection.find(query)
        return list(document)

    def get_multiple_data(self, collection, query, values_to_return=None):
        db_collection = self._db[collection]
        if values_to_return:
            document = db_collection.find(query, values_to_return)
        else:
            document = db_collection.find(query)
        return list(document)
