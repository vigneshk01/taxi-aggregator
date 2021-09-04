'use strict';

const MongoClient = require("mongodb").MongoClient;
const Crypto = require('crypto');
const ObjectID = require('mongodb').ObjectId;
const haversine = require('haversine');

let cachedDb = null;

async function connectToDatabase() {
      if (cachedDb) {
        return cachedDb;
      }
      // Connect to our MongoDB database hosted on MongoDB Atlas
      const client = await MongoClient
                            .connect(process.env.MONGODB_URI)
                            .catch(() => {
                                return confirmRideResponse(400, 'Error in connecting to db');
                            });
                            
      if (client) {
        // Specify which database we want to use
        const db = await client.db(process.env.MONGODB_DB);
        cachedDb = db;
        return db;    
      }
      else {
          return confirmRideResponse(400, 'Error in connecting to db');
      }
      
}

exports.handler = async (event) => {
    let body = JSON.parse(event.body);
    
    // Get an instance of our database
    const db = await connectToDatabase();
    
    let filter = {
                    APIKey: body.apiKey
                 };
                 
    let projection = {
                        projection: 
                                    {
                                        _id: 1
                                    }
                     };
                     
    const objID = await db.collection(process.env.COL_PSNG)
                          .findOne(filter, projection)
                          .catch(() => {
                                return confirmRideResponse(400, 'Error in finding user');
                          });
                          
    let start_loc = { latitude: body.startLat, longitude: body.startLng };
    let end_loc = { latitude: body.destLat, longitude: body.destLng };
    
    const distance = haversine(start_loc, end_loc);
    
    let cost = 0.0;
    
    switch(body.vehicleType) {
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
            return confirmRideResponse(400, 'Invalid vehicle type');
    }
    
    cost = cost.toFixed(2);
    
    let otpVal = Math.floor(100000 + Math.random() * 900000);
    let otpHash = Crypto.createHash('sha256').update(otpVal.toString()).digest('hex');
    
    if (objID._id) {
        let data = {
                    passenger_id: new ObjectID(objID._id),
                    start_address: body.startAddress,
                    dest_address: body.destAddress,
                    start_loc: {
                                type: "Point",
                                coordinates: [body.startLat, body.startLng]
                              },
                    dest_loc: {
                                type: "Point",
                                coordinates: [body.destLat, body.destLng]
                              },
                    booked_time: body.bookedTime,
                    schedule_time: body.scheduledTime,
                    start_time: "",
                    end_time: "",
                    vehicle_type: body.vehicleType,
                    vehicle_num: body.vehicleNum,
                    cost: cost,
                    passenger_rating: 5,
                    passenger_comments: 'Good',
                    OTPHash: otpHash
                 };
                 
        const insertResponse = await db.collection(process.env.COL_RIDES)
                        .insertOne(data)
                        .catch(() => {
                            return confirmRideResponse(400, 'Failed to confirm booking!');
                        });
                        
        if (insertResponse.acknowledged) {
            return confirmRideResponse(200, {"OTP": otpVal});
        }
        else {
            return confirmRideResponse(400, 'Failed to confirm booking!');
        }
    }
    else {
        return confirmRideResponse(400, 'Could not find user');
    }
};


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
