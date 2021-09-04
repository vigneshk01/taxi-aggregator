'use strict';

const MongoClient = require("mongodb").MongoClient;
const Crypto = require('crypto');

let cachedDb = null;

async function connectToDatabase() {
      if (cachedDb) {
        return cachedDb;
      }
      // Connect to our MongoDB database hosted on MongoDB Atlas
      const client = await MongoClient
                            .connect(process.env.MONGODB_URI)
                            .catch(() => {
                                return loginResponse(400, 'Error in connecting to db');
                            });
                            
      if (client) {
        // Specify which database we want to use
        const db = await client.db(process.env.MONGODB_DB);
        cachedDb = db;
        return db;    
      }
      else {
          return loginResponse(400, 'Error in connecting to db');
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
    
    if (body.user_type == process.env.USER_TYPE_PSNG) {
        col = process.env.COL_PSNG;
    }
    else if (body.user_type == process.env.USER_TYPE_TAXI) {
        col = process.env.COL_TAXI;
    }
    else {
        return loginResponse(400, 'Invalid user type');
    }
    
    let filter = {
                    username: body.username,
                    password: body.password,
                 };
    
    let data = {
                  $set: {
                            last_updated_timestamp: dt,
                            APIKey: apiKey
                        }
                };
  
    const updateResponse = await db.collection(col)
                        .updateOne(filter, data)
                        .catch(() => {
                            return loginResponse(400, "Login Failed!");
                        });
                        
    if (updateResponse.acknowledged) {
        return loginResponse(200, { APIKey: apiKey });
    }
    else {
        return loginResponse(400, "Login Failed!");
    }
};

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