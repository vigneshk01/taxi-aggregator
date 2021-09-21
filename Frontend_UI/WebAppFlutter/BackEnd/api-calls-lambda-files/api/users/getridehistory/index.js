'use strict';

const MongoClient = require("mongodb").MongoClient;
const ObjectID = require('mongodb').ObjectId;

exports.handler = async (event) => {
    
    let response = null;
    let client = null;
    
    try {
        // Get the body of event in JSON format
        const body = JSON.parse(event.body);
        
        console.log(event);
        
        // Create a Mongo client
        client = await MongoClient.connect(process.env.MONGODB_URI);
        
        // Connect to the Mongo database
        const db = await client.db(process.env.MONGODB_DB);
        
        let filter = {};
        let projection = {};
        
        if (body.user_type == process.env.USER_TYPE_PSNG) {
        
            // Filter data to get user ID
            filter = {
                APIKey: body.apiKey
            };
                     
            // Return user ID form database
            projection = {
                projection: {
                    _id: 1
                }
            };
    
            // Get user ID from database                     
            const objID = await db.collection(process.env.COL_PSNG)
                              .findOne(filter, projection);
                              
            console.log(JSON.stringify(objID));
        
            // Filter data to get ride with userID and time of booking
            filter = {
                passenger_id: new ObjectID(objID._id)
            };
        }
        else if (body.user_type == process.env.USER_TYPE_TAXI) {
            filter = {
                vehicle_num: body.vehicle_num
            };
        }
        else {
            response = getRideHistoryResponse(400, "Invalid user type");
            throw new Error("Invalid user type");
        }
        
        // Data points to return from database
        projection = {
            projection: {
                _id: 0,
                start_address: 1,
                dest_address: 1,
                start_loc: 1,
                dest_loc: 1,
                booked_time: 1,
                start_time: 1,
                end_time: 1,
                vehicle_type: 1,
                vehicle_num: 1,
                cost: 1,
                passenger_rating: 1,
                passenger_comments: 1,
                est_time: 1,
                total_distance: 1,
                status: 1
            }
        };
        
        // Get ride details from database
        const rideDetails = await db.collection(process.env.COL_RIDES)
                        .find(filter, projection).toArray();
        
        console.log(JSON.stringify(rideDetails));
        
        // If success return the details else return failure response
        if (rideDetails) {
            response = getRideHistoryResponse(200, rideDetails);
        }
        else {
            response = getRideHistoryResponse(400, {message: "Failed to get ride history!"});
            throw new Error("Failed to get ride history!");
        }
    
    }
    catch(error) {
        console.log(error);
        if(response == null) {
            response = getRideHistoryResponse(400, {message: "Failed to get ride history!"});
        }
    }
    finally {
        // Close mongo client
        if (client) {
            client.close();
        }
        return response;
    }
};

// Structure of response
function getRideHistoryResponse(code, data) {
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
