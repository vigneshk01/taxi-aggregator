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
                                return removeUserResponse(400, 'Error in connecting to db');
                            });
                            
      if (client) {
        // Specify which database we want to use
        const db = await client.db(process.env.MONGODB_DB);
        cachedDb = db;
        return db;    
      }
      else {
          return removeUserResponse(400, 'Error in connecting to db');
      }
      
}

exports.handler = async (event) => {
    let body = JSON.parse(event.body);
    
    // Get an instance of our database
    const db = await connectToDatabase();
    
    let col = process.env.COL_PSNG;
    
    if (body.user_type == process.env.USER_TYPE_PSNG) {
        col = process.env.COL_PSNG;
    }
    else if (body.user_type == process.env.USER_TYPE_TAXI) {
        col = process.env.COL_TAXI;
    }
    else {
        return removeUserResponse(400, 'Invalid user type');
    }
    
    let filter = {
                    username: body.username,
                    password: body.password,
                    APIKey: body.apiKey
                 };
                 
    let projection = {
                        projection: 
                                    {
                                        _id: 1
                                    }
                     };
                     
    const objID = await db.collection(col)
                          .findOne(filter, projection)
                          .catch(() => {
                                return removeUserResponse(400, 'Error in finding user');
                          });
    
    if (objID._id) {
        const removeResponse = await db.collection(col)
                        .deleteOne(objID)
                        .catch(() => {
                            return removeUserResponse(400, 'Error in removing user');
                        });
                        
        if (removeResponse.acknowledged) {
            return removeUserResponse(200, 'Successfully removed user!');
        }
        else {
            return removeUserResponse(400, 'Failed to remove user!');
        }
    }
    else {
        return removeUserResponse(400, 'Could not find user');
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
