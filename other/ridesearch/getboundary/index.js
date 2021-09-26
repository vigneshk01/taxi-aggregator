'use strict';

const MongoClient = require("mongodb").MongoClient;

exports.handler = async (event) => {
    
    let response = null;
    let client = null;
    
    try {
        // Create a Mongo client
        client = await MongoClient
                                .connect(process.env.MONGODB_URI);
        
        // Connect to the Mongo database
        const db = await client.db(process.env.MONGODB_DB);
    
        // No filter get all
        let query = {};
    
        // Datapoint to return from database
        let projection = {
            projection: {
                _id: 0,
            }
        };
  
        // Get boundary fom database
        const boundary = await db.collection(process.env.COL_BND).findOne(query, projection);
        
        console.log(JSON.stringify(boundary));
        
        // If success return boundary ese return failure response
        if (boundary) {
            response = getBoundaryResponse(200, boundary);
        }
        else {
            response = getBoundaryResponse(400, {message: "Failed to get boundary!"});
        }
    }
    catch(error) {
        console.log(error);
        if (response == null) {
            response = getBoundaryResponse(400, {message: "Failed to get boundary!"});
        }
    }
    finally {
        //Close mongo client
        if(client) {
            await client.close();
        }
        return response;
    }
};

// Structure of response
function getBoundaryResponse(code, data) {
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
