'use strict';

const MongoClient = require("mongodb").MongoClient;
const Crypto = require('crypto');

exports.handler = async (event) => {
    
    let response = null;
    let client = null;
    let session = null;
    
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
                response = removeUserResponse(400, {message: "Invalid user type"});
                throw new Error("Invalid user type!");
        }
    
        // Structure of data filter
        let filter = {
            username: body.username,
            password: body.password,
            APIKey: body.apiKey
        };
        
        // Structure of data to show
        let projection = {
            projection: {
                _id: 1
            }
        };
        
        // Start session
        session = client.startSession();
    
        // transaction options
        const transactionOptions = {
            readPreference: 'primary',
            readConcern: { level: 'local' },
            writeConcern: { w: 'majority' }
        };
 
        const transactionResults = await session.withTransaction(async () => {
                         
            const objID = await db.collection(col).findOne(filter, projection);
        
            console.log(JSON.stringify(objID));
        
            const removeResponse = await db.collection(col).deleteOne(objID, {session});
        
            console.log(JSON.stringify(removeResponse));
            
        }, transactionOptions);
                            
        if (transactionResults) {
            response = removeUserResponse(200, {message: "Successfully removed user!"});
        }
        else {
            response = removeUserResponse(400, {message: "Failed to remove user!"});
            throw new Error('Transaction failed!');
        }
    }
    catch(error) {
        console.log(error);
        if (response == null) {
            response = removeUserResponse(400, {message: "Failed to remove user!"});
        }
    }
    finally {
        //End mongo session
        if(session) {
            await session.endSession();
        }
        // Close mongo client
        if(client) {
            await client.close();
        }
        return response;
    }
};


function removeUserResponse(code, data) {
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
