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
        client = await MongoClient
                                .connect(process.env.MONGODB_URI);
        
        // Connect to the Mongo database
        const db = await client.db(process.env.MONGODB_DB);
        
        
        // Filter data for particular vehicle number
        let query = {
            OTPHash: body.otpHash,
            vehicle_num: body.vehicle_num
        };
        
        // Datapoints to retur from database
        let projection = {
            projection: {
                _id: 0,
                current_vehicle_location: 1,
                instruction: 1,
                distance: 1,
                duration: 1
            }
        };
      
        // Get ride location from rides collection
        const resp = await db.collection(process.env.COL_RIDES).findOne(query, projection);
                            
        console.log(JSON.stringify(resp));
        
        // If success return location else return failure response
        if(resp.current_vehicle_location) {
            response = getRideLocResponse(200, resp);
        }
        else {
            response = getRideLocResponse(400, {message: "Failed to get location!"});
        }
    }
    catch(error) {
        console.log(error);
        if (response == null ) {
            response = getRideLocResponse(200, {message: "Failed to get location!"});
        }
    }
    finally {
        // Close mongo client
        if (client) {
            await client.close();
        }
        return response;
    }
    
};

// Structure of response
function getRideLocResponse(code, data) {
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
