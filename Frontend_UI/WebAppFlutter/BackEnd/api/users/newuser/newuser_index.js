'use strict';

const MongoClient = require("mongodb").MongoClient;
const Crypto = require("crypto");

let cachedDb = null;

async function connectToDatabase() {
      if (cachedDb) {
        return cachedDb;
      }
      // Connect to our MongoDB database hosted on MongoDB Atlas
      const client = await MongoClient
                            .connect(process.env.MONGODB_URI)
                            .catch(() => {
                                return newUserResponse(400, 'Error in connecting to db');
                            });
                            
      if (client) {
        // Specify which database we want to use
        const db = await client.db(process.env.MONGODB_DB);
        cachedDb = db;
        return db;    
      }
      else {
          return newUserResponse(400, 'Error in connecting to db');
      }
      
}

exports.handler = async (event) => {
    let body = JSON.parse(event.body);
    
    // Get an instance of our database
    const db = await connectToDatabase();
    
    let col = process.env.COL_PSNG;
    
    let dt = new Date().toISOString();
    let secretKey = process.env.SECRETKEY;
    let secretHash = Crypto.createHash('sha256').update(secretKey+dt).digest('hex');
    let apiKey = Crypto.createHash('sha256').update(body.username+body.password+secretHash).digest('hex');
    
    let data = {};
    if (body.user_type == process.env.USER_TYPE_PSNG) {
        
        col = process.env.COL_PSNG;
        
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
        
        col = process.env.COL_TAXI;
        
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
        return newUserResponse(400, 'Invalid user type');
    }
  
    await db.collection(col)
                        .insertOne(data)
                        .catch(() => {
                            return newUserResponse(400, 'Error in adding user to db');
                        });
   
    return newUserResponse(200, 'Successfully added user');
};

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
