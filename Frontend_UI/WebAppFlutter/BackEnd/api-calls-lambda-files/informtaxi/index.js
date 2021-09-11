'use strict';

const MongoClient = require("mongodb").MongoClient;
const AWS = require('aws-sdk');
AWS.config.update({region: process.env.REGION});

exports.handler = async (event) => {
    
    let response = null;
    let client = null;
    
    try {
        // Get the body of event in JSON format
        const body = JSON.parse(event.Records[0].Sns.Message);
        
        console.log(JSON.stringify(event));
        
        // Create a Mongo client
        client = await MongoClient
                                .connect(process.env.MONGODB_URI);
        
        // Connect to the Mongo database
        const db = await client.db(process.env.MONGODB_DB);
        
        // Filter data to get a taxi
        let query = {
            vehicle_num: body.vehicle_num
        };
        
        // Datapoints to return from database
        let projection = {
            projection: {
                _id: 0,
                location: 1
            }
        };
      
        // Get current location of a taxi from the taxi collection
        const resp = await db.collection(process.env.COL_TAXI).findOne(query, projection);
        
        console.log(JSON.stringify(resp));
        
        // If success then publish message to SNS else return failure response
        if (resp) {
            
            // Message to publish
            let message = {
                start_loc: {"lat": resp.location.coordinates[0],"lng": resp.location.coordinates[1]},
                end_loc: body.start_loc,
                OTPHash: body.OTPHash,
                vehicle_num: body.vehicle_num,
                status: "WAITING_FOR_RIDE"
            };
            
            // SNS parameters
            let params = {
                Message: JSON.stringify(message),
                Subject: "Simulate travel",
                TopicArn: process.env.TOPIC_ARN
            };
            
            // Publih esage to SNS and get a promise    
            let publishTextPromise = new AWS.SNS().publish(params).promise();
            
            // Wait for the response  to be received from SNS
            const pubResp = await publishTextPromise;
            
            console.log(JSON.stringify(pubResp));
            
            // Successful response
            response = informTaxiResponse(200, "Successfully informed taxi");
        }
        else {
            response = informTaxiResponse(400, "Failed to get taxi location!");
        }
    }
    catch(error) {
        console.log(error);
        if (response == null) {
            response = informTaxiResponse(400, "Failed to inform!");
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
function informTaxiResponse(code, data) {
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
    console.log(code+'\n'+data);
    return response;
}
