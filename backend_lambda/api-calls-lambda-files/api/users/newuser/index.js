'use strict';

const MongoClient = require("mongodb").MongoClient;
const Crypto = require("crypto");

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
        
        // Get passenger collection name
        let col = process.env.COL_PSNG;
        
        // Create SHA256 bases API Key that changes on each login
        let dt = new Date().toISOString();
        let secretKey = process.env.SECRETKEY;
        let secretHash = Crypto.createHash('sha256').update(secretKey+dt).digest('hex');
        let apiKey = Crypto.createHash('sha256').update(body.username+body.password+secretHash).digest('hex');
        
        // Struture of update data as per user (Passenger/Taxi)
        let data = {};
        if (body.user_type == process.env.USER_TYPE_PSNG) {
            // Get passenger collection name
            col = process.env.COL_PSNG;
            // Passenger new data structure
            data = {
                firstname: body.firstname,
                lastname: body.lastname,
                username: body.username,
                password: body.password,
                APIKey: apiKey,
                last_updated_timestamp: dt
            };
        }
        else if (body.user_type == process.env.USER_TYPE_TAXI) {
            // Get Taxi collection name
            col = process.env.COL_TAXI;
            // Taxi new data structure
            data = {
                firstname: body.firstname,
                lastname: body.lastname,
                username: body.username,
                password: body.password,
                vehicle_num: body.vehicle_num,
                vehicle_type: body.vehicle_type,
                driving_license_num: body.driving_license_num,
                location: {
                    type: "Point",
                    coordinates: [body.lat, body.lng]
                },
                last_updated_timestamp: dt,
                APIKey: apiKey,
                status: body.status,
            };
        }
        else {
            response = newUserResponse(400, {message: "Invalid user type!"});
            throw new Error("Invalid user type!");
        }
      
        // start a mongo session
        session = client.startSession();
        
        // set mongo transaction options
        const transactionOptions = {
            readPreference: 'primary',
            readConcern: { level: 'local' },
            writeConcern: { w: 'majority' }
        };
        
        // Transaction operations
        const transactionResults =await session.withTransaction(async () => {
            // Insert new user data to database
            const insertResponse = await db.collection(col).insertOne(data, {session});
            
            console.log(JSON.stringify(insertResponse));
        }, transactionOptions);
        
        console.log(transactionResults);
           
        // If success then return response success else return response failure
        if(transactionResults) {
            response = newUserResponse(200, {message: "Create success!"});
        }
        else {
            response = newUserResponse(400, {message: "Failed to create user!"});
            throw new Error("Failed to create user!");
        }
    }
    catch(error) {
        console.log(error);
        if(response == null) {
            response = newUserResponse(400, {message: "Failed to create user!"});
        }
        if (session) {
            await session.abortTransaction();
        }
    }
    finally {
        // End the mongo session
        if(session) {
            await session.endSession();
        }
        // Close the Mongo connections from this instance
        if(client) {
            await client.close();
        }
        return response;
    }
};

// Structure of response
function newUserResponse(code, data) {
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
