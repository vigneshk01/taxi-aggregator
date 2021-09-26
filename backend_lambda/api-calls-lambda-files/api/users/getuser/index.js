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
                response = getUserResponse(400, {message: "Invalid user type"});
                throw new Error("Invalid user type!");
        }
        
        // Filters to query the mongo database
        let query = {
            APIKey: body.apiKey
        };
        
        // Project only certain data points
        let projection = {
            projection: {
                _id: 0,
                firstname: 1,
                lastname: 1,
                vehicle_num: 1,
                vehicle_type: 1,
                driving_license_num: 1,
                status: 1
            }
        };
      
        // Get user details from database
        const user = await db.collection(col).findOne(query, projection);
        
        console.log("Response:\n"+JSON.stringify(user));
        
        // If respose obtained that return response
        // else return user not found
        if(user) {
            response = getUserResponse(200, user);
        }
        else {
            response = getUserResponse(400, {message: "Failed to get user!"});
            throw new Error("Invalid response");
        }
    }
    catch(error) {
        console.log(error);
        if(response == null) {
            response = getUserResponse(400, {message: "Failed to get user!"});
        }
    }
    finally {
        if (client) {
            client.close();
        }
        return response;
    }
};

// Structure of response
function getUserResponse(code, data) {
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
