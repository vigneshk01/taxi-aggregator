'use strict';

const MongoClient = require("mongodb").MongoClient;

exports.handler = async (event) => {
    
    let response = null;
    let client = null;
    let session = null;
    
    try {
        
        // Get the body of event in JSON format
        const body = JSON.parse(event.body);
        
        console.log(event);
        
        // Create a Mongo client
        client = await MongoClient.connect(process.env.MONGODB_URI);
        
        // Connect to the Mongo database
        const db = await client.db(process.env.MONGODB_DB);
        
        let col = null;
        
        // Obtain collection name as per type of user (Passenger/Taxi)
        switch(body.user_type) {
            case process.env.USER_TYPE_PSNG:
                response = updateUserResponse(400, {message: "Not supported"});
                throw new Error("Not supported");
            case process.env.USER_TYPE_TAXI:
                col = process.env.COL_TAXI;
                break;
            default:
                response = updateUserResponse(400, {message: "Invalid user type"});
                throw new Error("Invalid user type!");
        }
        
        // Structure of filter to select data in database
        let updatefilter = {
            APIKey: body.apiKey,
            vehicle_num: body.vehicle_num
        };
        
        // Current date and time
        let dt = new Date().toISOString();             
        
        // Struture of update data
        let data = {};
        switch(body.update_type) {
            case "taxiLoc":
                data = {
                    $set: {
                        location: {
                            type: "Point",
                            coordinates: [body.lat, body.lng]
                        },
                        last_updated_timestamp: dt,
                        status: body.status
                    }
                };
                break;
            default:
                response =  updateUserResponse(400, {message: "Invalid update type!"});
                throw new Error("Invalid update type!");
        }
        
        // start a mongo session
        session = client.startSession();
        
        // set mongo transaction options
        const transactionOptions = {
            readPreference: 'primary',
            readConcern: { level: 'local' },
            writeConcern: { w: 'majority' }
        };
        
        const transactionResults =await session.withTransaction(async () => {
            // Change user data in database
            const updateResponse = await db.collection(col).updateOne(updatefilter, data, {session});
            
            console.log(JSON.stringify(updateResponse));
            
        }, transactionOptions);
                            
        if (transactionResults) {
            response = updateUserResponse(200, {message: "Successful update!"});
        }
        else {
            response = updateUserResponse(400, {message: "Update Failed!"});
            throw new Error("Update Failed!");
        }
    }
    catch(error) {
        console.log(error);
        if (response == null) {
            response = updateUserResponse(400, {message: "Update Failed!"});
        }
    }
    finally {
        // End mongo session
        if (session) {
            await session.endSession();
        }
        // Close connections using this mongo instance
        if (client) {
            await client.close();
        }
        return response;
    }
};

// Structure of res
function updateUserResponse(code, data) {
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