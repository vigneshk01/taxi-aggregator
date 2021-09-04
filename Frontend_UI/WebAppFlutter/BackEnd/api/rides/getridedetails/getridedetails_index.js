'use strict';

const MongoClient = require("mongodb").MongoClient;
const ObjectID = require('mongodb').ObjectID;

let cachedDb = null;

async function connectToDatabase() {
      if (cachedDb) {
        return cachedDb;
      }
      // Connect to our MongoDB database hosted on MongoDB Atlas
      const client = await MongoClient
                            .connect(process.env.MONGODB_URI)
                            .catch(() => {
                                return getRideDetailsResponse(400, 'Error in connecting to db');
                            });
                            
      if (client) {
        // Specify which database we want to use
        const db = await client.db(process.env.MONGODB_DB);
        cachedDb = db;
        return db;    
      }
      else {
          return getRideDetailsResponse(400, 'Error in connecting to db');
      }
      
}

exports.handler = async (event) => {
    let body = JSON.parse(event.body);
    
    // Get an instance of our database
    const db = await connectToDatabase();
    
    let filter = {
                    APIKey: body.apiKey
                 };
                 
    let projection = {
                        projection: 
                                    {
                                        _id: 1
                                    }
                     };
                     
    const objID = await db.collection(process.env.COL_PSNG)
                          .findOne(filter, projection)
                          .catch(() => {
                                return getRideDetailsResponse(400, 'Error in finding user');
                          });
    
    if (objID._id) {
        filter = {
                    userID: new ObjectID(objID._id),
                    bookedTime: body.bookedTime
                 };
        
        projection = {
                        projection: {
                            _id: 0,
                            startAddress: 1,
                            destAddress: 1,
                            startLoc: 1,
                            destLoc: 1,
                            bookedTime: 1,
                            startTime: 1,
                            endTime: 1,
                            vehicle_type: 1,
                            vehicle_num: 1,
                            cost: 1,
                            passenger_rating: 1,
                            passenger_comments: 1
                        }
                     };
        
        const rideDetails = await db.collection(process.env.COL_RIDES)
                        .findOne(filter, projection)
                        .catch(() => {
                            return getRideDetailsResponse(400, 'Error in finding ride details');
                        });
                        
        if (rideDetails.bookedTime) {
            return getRideDetailsResponse(200, rideDetails);
        }
        else {
            return getRideDetailsResponse(400, 'Failed to get ride details!');
        }
    }
    else {
        return getRideDetailsResponse(400, 'Could not find user');
    }
};


function getRideDetailsResponse(code, data) {
    const response = {
                        "isBase64Encoded": false,
                        "statusCode": code,
                         "headers": {
                            "Access-Control-Allow-Origin": "*",
                            "Access-Control-Allow-Headers": "Content-Type, Access-Control-Allow-Origin, Accept",
                            "Access-Control-Allow-Methods": "POST, OPTIONS"
                        },
                        "body": JSON.stringify(data),
                     };
    return response;
}
