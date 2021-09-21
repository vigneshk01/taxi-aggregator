'use strict';

const MongoClient = require("mongodb").MongoClient;

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
        
        
        // Filter data to get ride with userID and time of booking
        let filter = {vehicle_num: body.vehicle_num, status: {$not: {$eq: "COMPLETED"}}};
        
        let sort = {booked_time: -1};
        
        // Data points to return from database
        let projection = {
            projection: {
                _id: 0,
                start_address: 1,
                dest_address: 1,
                start_loc: 1,
                dest_loc: 1,
                booked_time: 1,
                start_time: 1,
                end_time: 1,
                current_vehicle_location: 1,
                status: 1
            }
        };
        
        // Get ride details from database
        const rideDetails = await db.collection(process.env.COL_RIDES)
                        .find(filter, projection).sort(sort).limit(1).toArray();
                        
        filter = {vehicle_num: body.vehicle_num};
            
        projection = {
            projection: {
                _id: 0, 
                location: 1, 
                status: 1
            }
        };
              
        // Get taxi location from database
        const taxiLoc = await db.collection(process.env.COL_TAXI)
                        .findOne(filter, projection);
        
        console.log(JSON.stringify(rideDetails));
        
        console.log(JSON.stringify(taxiLoc));
        
        // If success return the details else return failure response
        if (rideDetails && taxiLoc) {
            
            let taxiDets = {
                current_ride: rideDetails,
            };
            Object.assign(taxiDets, taxiLoc);
            response = getCurrentTaxiDataResponse(200, taxiDets);
        }
        else {
            response = getCurrentTaxiDataResponse(400, {message: "Failed to get ride details!"});
            throw new Error("Failed to get ride details!");
        }
    
    }
    catch(error) {
        console.log(error);
        if(response == null) {
            response = getCurrentTaxiDataResponse(400, {message: "Failed to get ride details!"});
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
function getCurrentTaxiDataResponse(code, data) {
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
