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
        
        // Structure of data to filter database data
        let query = {
            location: {
                $near : {
                    $geometry: { 
                        type: "Point",  
                        coordinates: [ body.lat, body.lng ] 
                    },
                    $minDistance: 0,
                    $maxDistance: 5000
                }
            }
        };
        
        // Strucutre of datapoints to return
        let projection = {
            projection: {
                _id: 0,
                vehicle_num: 1,
                vehicle_type: 1,
                location: 1,
            }
        };
      
        // Get nearby rides from database
        const nearbyRides = await db.collection(process.env.COL_TAXI)
                                    .find(query, projection)
                                    .toArray();
       
        // If successful return array of rides else return response failed
        if (nearbyRides) {
            response = nearbyRidesResponse(200, nearbyRides);
        }
        else {
            response = nearbyRidesResponse(400, {message: "Failed to get nearby rides!"});
            throw new Error("Failed to get nearby rides");
        }
    }
    catch(error) {
        console.log(error);
        if (response == null) {
            response = nearbyRidesResponse(400, {message: "Failed to get nearby rides!"});
        }
    }
    finally {
        // Close connections from this mongo instance
        if (client) {
            await client.close();
        }
        return response;
    }
};

// Structure of response
function nearbyRidesResponse(code, data) {
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