'use strict';

const MongoClient = require("mongodb").MongoClient;
const ObjectID = require('mongodb').ObjectId;
const AWS = require('aws-sdk');
AWS.config.update({region: process.env.REGION});

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
        
        // Filter data as per users API key
        let queryfilter = {
            APIKey: body.apiKey
        };
        
        // datapoint to return from database             
        let projection = {
            projection: {
                _id: 1
            }
        };
        
        // Get users ID in database                 
        const objID = await db.collection(process.env.COL_PSNG).findOne(queryfilter, projection);
                              
        // Filter data as per passeer ID and Otp for the ride
        let updatefilter = {
            passenger_id: new ObjectID(objID._id),
            OTPHash: body.OTPHash
        };
        
        // Set data to update as per the update type             
        let data = {};
        let resData = {};
        switch(body.update_type) {
            case "startTime":
                data = {
                    $set: {
                        start_time: body.start_time,
                        status: "STARTED_RIDE"
                    }
                };
                resData = {
                    start_time: body.start_time  
                };
                break;
            case "endTime":
                data = {
                    $set: {
                        end_time: body.end_time,
                        status: "ENDED_RIDE"
                    }
                };
                
                resData = {
                    end_time: body.end_time  
                };
                break;
            case "feedback":
                data = {
                    $set: {
                        passenger_rating: body.passenger_rating,
                        passenger_comments: body.passenger_comments,
                        status: "COMPLETED"
                    }
                };
                
                resData = {
                    passenger_rating: body.passenger_rating,
                    passenger_comments: body.passenger_comments
                };
                break;
            default:
                response = updateRideResponse(400, {message: "Invalid update type!"});
                throw new Error("Invalid update type!");
        }
      
        // Update the ride details
        const updateResponse = await db.collection(process.env.COL_RIDES).updateOne(updatefilter, data);
        
        console.log(JSON.stringify(updateResponse));
                            
        // If success then return updated data else return failure response
        if (updateResponse.modifiedCount == 1) {
            response = updateRideResponse(200, resData);
            
            if (body.update_type == "startTime") {
                let start_loc = { latitude: body.start_lat, longitude: body.start_lng };
                let end_loc = { latitude: body.dest_lat, longitude: body.dest_lng };
            
                 // Message to publish
                let message = {
                    start_loc: start_loc,
                    end_loc: end_loc,
                    OTPHash: body.OTPHash,
                    vehicle_num: body.vehicle_num,
                    status: "STARTED_RIDE"
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
            }
            else if(body.update_type == "endTime") {
                // Filter data to get particular taxi                     
                let filterTaxi = {
                    vehicle_num: body.vehicle_num
                };
                        
                // Update data for taxi status            
                let updStatusData = {
                    $set: {
                        status: "ACTIVE"
                    }
                };
              
                // Update taxi status as BOOKED in database
                const txiUpdRes = await db.collection(process.env.COL_TAXI)
                                    .findOneAndUpdate(filterTaxi, updStatusData);
                                    
                console.log(JSON.stringify(txiUpdRes));
            }
            
        }
        else {
            response = updateRideResponse(400, {message: "Update Failed!"});
        }
    }
    catch(error) {
        console.log(error);
        if (response == null) {
            response = updateRideResponse(400, {message: "Update Failed!"});
        }
    }
    finally {
        // Close mogo client
        if (client) {
            await client.close();
        }
        return response;
    }
};

// Structure of response
function updateRideResponse(code, data) {
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