'use strict';

const MongoClient = require("mongodb").MongoClient;
const ObjectID = require('mongodb').ObjectId;

let cachedDb = null;

async function connectToDatabase() {
      if (cachedDb) {
        return cachedDb;
      }
      // Connect to our MongoDB database hosted on MongoDB Atlas
      const client = await MongoClient
                            .connect(process.env.MONGODB_URI)
                            .catch(() => {
                                return updateRideResponse(400, 'Error in connecting to db');
                            });
                            
      if (client) {
        // Specify which database we want to use
        const db = await client.db(process.env.MONGODB_DB);
        cachedDb = db;
        return db;    
      }
      else {
          return updateRideResponse(400, 'Error in connecting to db');
      }
      
}

exports.handler = async (event) => {
    let body = JSON.parse(event.body);
    
    // Get an instance of our database
    const db = await connectToDatabase();
    
    let queryfilter = {
                    APIKey: body.apiKey
                 };
                 
    let projection = {
                        projection: 
                                    {
                                        _id: 1
                                    }
                     };
                     
    const objID = await db.collection(process.env.COL_PSNG)
                          .findOne(queryfilter, projection)
                          .catch(() => {
                                return updateRideResponse(400, 'Error in finding user');
                          });
                          
    let updatefilter = {
                    passenger_id: new ObjectID(objID._id),
                    OTPHash: body.OTP
                 };
                 
    let data = {};
    let resData = {};
    switch(body.updateType) {
        case "startTime":
            data = {
                        $set: {
                            start_time: body.startTime
                        }
                   };
            resData = {
                        start_time: body.startTime  
                      };
            break;
        case "endTime":
            data = {
                        $set: {
                            end_time: body.endTime
                        }
                   };
            
            resData = {
                        end_time: body.endTime  
                      };
            break;
        case "feedback":
            data = {
                        $set: {
                            passenger_rating: body.passengerRating,
                            passenger_comments: body.passengerComments
                        }
                   };
            
            resData = {
                            passenger_rating: body.passengerRating,
                            passenger_comments: body.passengerComments
                      };
            break;
        default:
            return updateRideResponse(400, 'Invalid update type');
    }
  
    const updateResponse = await db.collection(process.env.COL_RIDES)
                        .updateOne(updatefilter, data)
                        .catch(() => {
                            return updateRideResponse(400, "Update Failed!");
                        });
                        
    if (updateResponse.acknowledged) {
        return updateRideResponse(200, resData);
    }
    else {
        return updateRideResponse(400, "Update Failed!");
    }
};

function updateRideResponse(code, data) {
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