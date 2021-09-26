'use strict';

const MongoClient = require("mongodb").MongoClient;

exports.handler = async (event) => {
    
    let response = null;
    let client = null;
    
    try {
        
        // Create a Mongo client
        client = await MongoClient.connect(process.env.MONGODB_URI);
        
        // Connect to the Mongo database
        const db = await client.db(process.env.MONGODB_DB);
    
        // No need for a filter. Get all results
        let query = {};
        
        // Return only speific data points from database
        let projection = {
            projection: {
                _id: 0,
            }
        };
      
        // Get taxis from database
        const taxisList = await db.collection(process.env.COL_TAXI)
                            .find(query, projection)
                            .toArray();
                            
        console.log(JSON.stringify(taxisList));
       
        // If success return list else retun failure response
        if (taxisList) {
            response = getTaxisResponse(200, taxisList);
        }
        else {
            response = getTaxisResponse(400, {message: "Failed to get all taxis!"});
            throw new Error("Failed to get all taxis!");
        }
    }
    catch(error) {
        console.log(error);
        if (response == null) {
            response = getTaxisResponse(400, {message: "Failed to get all taxis!"});
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
function getTaxisResponse(code, data) {
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
