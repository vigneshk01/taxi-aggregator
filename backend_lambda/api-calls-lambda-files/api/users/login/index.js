'use strict';

const MongoClient = require("mongodb").MongoClient;
const Crypto = require('crypto');

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
    
        // Create new API key for this login
        let dt = new Date().toISOString();
        let secretKey = process.env.SECRETKEY;
        let secretHash = Crypto.createHash('sha256').update(secretKey+dt).digest('hex');
        let apiKey = Crypto.createHash('sha256').update(body.username+body.password+secretHash).digest('hex');
        
        let col = null;
        
        // Obtain collection name as per type of user (Passenger/Taxi)
        switch(body.user_type) {
            case process.env.USER_TYPE_PSNG:
                col = process.env.COL_PSNG;
                break;
            case process.env.USER_TYPE_TAXI:
                col = process.env.COL_TAXI;
                break;
            default:
                response = loginResponse(400, {message: "Invalid user type"});
                throw new Error("Invalid user type!");
        }
        
        // Filter data
        let filter = {
            username: body.username,
            password: body.password,
        };
        
        // Update data
        let data = {
            $set: {
                last_updated_timestamp: dt,
                APIKey: apiKey
            }
        };
      
        // Update APIKey of user
        const updateResponse = await db.collection(col)
                            .updateOne(filter, data);
        
        console.log(JSON.stringify(updateResponse));
        
        // If success then return the API Key else return failure response
        if (updateResponse.modifiedCount == 1) {
            response = loginResponse(200, { APIKey: apiKey });
        }
        else {
            response = loginResponse(400, {message: "Login Failed!"});
        }
    }
    catch(error) {
        console.log(error);
        if (response == null) {
            response = loginResponse(400, {message: "Login Failed!"});
        }
    }
    finally {
        // close mongo client
        if (client) {
            await client.close();
        }
        return response;
    }
};

// Structure of response
function loginResponse(code, data) {
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