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
        
        // Filter data to get user ID
        let filter = {
            APIKey: body.apiKey
        };
                 
        // Return user ID form database
        let projection = {
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
            passenger_id: new ObjectID(objID._id),
            booked_time: body.booked_time
        };
        
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
                passenger_comments: 1
            }
        };
        
        // Get ride details from database
        const rideDetails = await db.collection(process.env.COL_RIDES)
                        .findOne(filter, projection);
        
        console.log(JSON.stringify(rideDetails));
        
        // If success return the details else return failure response
        if (rideDetails) {
            response = getRideDetailsResponse(200, rideDetails);
        }
        else {
            response = getRideDetailsResponse(400, {message: "Failed to get ride details!"});
            throw new Error("Failed to get ride details!");
        }
    
    }
    catch(error) {
        console.log(error);
        if(response == null) {
            response = getRideDetailsResponse(400, {message: "Failed to get ride details!"});
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
