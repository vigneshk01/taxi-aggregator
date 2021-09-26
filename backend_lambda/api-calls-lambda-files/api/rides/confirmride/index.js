'use strict';

const MongoClient = require("mongodb").MongoClient;
const Crypto = require('crypto');
const ObjectID = require('mongodb').ObjectId;
const haversine = require('haversine');
const AWS = require('aws-sdk');
AWS.config.update({region: process.env.REGION});

exports.handler = async (event) => {
    let response = null;
    let client = null;
    let session = null;
    let otpVal = null;
    let otpHash = null;
    let taxiLoc = null;
    
    try {
        
        // Get the body of event in JSON format
        const body = JSON.parse(event.body);
        
        console.log(event);
        
        // Create a Mongo client
        client = await MongoClient.connect(process.env.MONGODB_URI);
        
        // Connect to the Mongo database
        const db = await client.db(process.env.MONGODB_DB);
        
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
        
            // Filter data
            let filter = {
                APIKey: body.apiKey
            };
                      
            // Datapoints returned from database   
            let projection = {
                projection: {
                    _id: 1
                }
            };
            
            // Get user ID                 
            const objID = await db.collection(process.env.COL_PSNG)
                                  .findOne(filter, projection);
                                  
            // Filter data to get particular taxi                     
            let queryTaxiLoc = {
                vehicle_num: body.vehicle_num,
                status: "BOOKED"
            };
            
            // datapoints to return on update
            let projectionTaxiLoc = {
                projection: {
                    _id: 0,
                    location: 1
                }
            };
          
            // Update taxi status as BOOKED in database
            const resptaxiLoc = await db.collection(process.env.COL_TAXI)
                                .findOne(queryTaxiLoc, projectionTaxiLoc);
                                
            console.log(JSON.stringify(resptaxiLoc));
            
            // If no taxi found then abort transaction
            if(resptaxiLoc) {                    
                taxiLoc = resptaxiLoc.location.coordinates;
                console.log(JSON.stringify(taxiLoc));
            }
            else {
                response = confirmRideResponse(400, {message: "Failed to find taxi"});
                throw new Error("Tansaction aborted Taxi location!");
            }

            // Calcuate the cost of the ride from haversine formula of distance                                  
            let start_loc = { latitude: body.start_lat, longitude: body.start_lng };
            let end_loc = { latitude: body.dest_lat, longitude: body.dest_lng };
            
            const distance = haversine(start_loc, end_loc);
            
            let cost = 0.0;
            
            switch(body.vehicle_type) {
                case "UTILITY":
                    cost = 25 * distance;
                    break;
                case "DELUXE":
                    cost = 35 * distance;
                    break;
                case "LUXURY":
                    cost = 45 * distance;
                    break;
                default:
                    response = confirmRideResponse(400, {message: 'Invalid vehicle type'});
            }
        
            // Roud of the cost to two decimal places
            cost = cost.toFixed(2);
            
            // Generate random OTP value
            otpVal = Math.floor(100000 + Math.random() * 900000);
            otpHash = Crypto.createHash('sha256').update(otpVal.toString()).digest('hex');
        
            // Data to create in Rides collection
            let data = {
                passenger_id: new ObjectID(objID._id),
                start_address: body.start_address,
                dest_address: body.dest_address,
                start_loc: {
                    type: "Point",
                    coordinates: [body.start_lat, body.start_lng]
                },
                dest_loc: {
                    type: "Point",
                    coordinates: [body.dest_lat, body.dest_lng]
                },
                booked_time: body.booked_time,
                schedule_time: body.scheduled_time,
                start_time: "",
                end_time: "",
                vehicle_type: body.vehicle_type,
                vehicle_num: body.vehicle_num,
                cost: cost,
                passenger_rating: "5",
                passenger_comments: "Good",
                OTPHash: otpHash,
                status: "WAITING_FOR_RIDE",
                current_vehicle_location: {
                    type: "Point",
                    coordinates: [taxiLoc[0], taxiLoc[1]]
                }
            };
                     
            const insertResp = await db.collection(process.env.COL_RIDES)
                            .insertOne(data, {session});
                            
            console.log(JSON.stringify(insertResp));
                            
            if(insertResp.acknowledged == false) {
                throw new Error("Failed to create ride!");
            }
        
            let message = {
                start_loc: {"lat": body.start_lat,"lng": body.start_lng},
                OTPHash: otpHash,
                vehicle_num: body.vehicle_num,
                status: "WAITING_FOR_RIDE"
            };
                            
            let params = {
                Message: JSON.stringify(message),
                Subject: "Book taxi",
                TopicArn: process.env.TOPIC_ARN
            };
    
            let publishTextPromise = new AWS.SNS().publish(params).promise();
    
            const resp = await publishTextPromise;
            
            console.log(JSON.stringify(resp));
            
            if(resp == null) {
                throw new Error("Failed to inform taxi!");
            }
            
        }, transactionOptions);
        
        console.log(JSON.stringify(transactionResults));
        
        // If transaction results failed then abort transaction else return otp value
        if (transactionResults) {
            response = confirmRideResponse(200, {OTP: otpVal.toString()});
        }
        else {
            response = confirmRideResponse(400, {message: "Failed to confirm!"});
            throw new Error("Transaction aborted as transaction results failed!");
        }
    }
    catch(error) {
        console.log(error);
        if (response == null) {
            response = confirmRideResponse(400, {message: "Failed to confirm!"});
        }
        if (session) {
            await session.abortTransaction();
        }
    }
    finally {
        // End mongo session
        if (session) {
            await session.endSession();
        }
        // Close mongo client
        if (client) {
            await client.close();
        }
        return response;
    }
};

// Structure of response
function confirmRideResponse(code, data) {
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