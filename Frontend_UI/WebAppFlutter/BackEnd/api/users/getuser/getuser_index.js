'use strict';

const MongoClient = require("mongodb").MongoClient;

let cachedDb = null;

async function connectToDatabase() {
      if (cachedDb) {
        return cachedDb;
      }
      // Connect to our MongoDB database hosted on MongoDB Atlas
      const client = await MongoClient
                            .connect(process.env.MONGODB_URI)
                            .catch(() => {
                                return getUserResponse(400, 'Error in connecting to db');
                            });
                            
      if (client) {
        // Specify which database we want to use
        const db = await client.db(process.env.MONGODB_DB);
        cachedDb = db;
        return db;    
      }
      else {
          return getUserResponse(400, 'Error in connecting to db');
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
        return getUserResponse(400, 'Invalid user type');
    }
    
    let query = {
                    APIKey: body.apiKey
                };
    
    let projection = {
                        projection: {
                                        _id: 0,
                                        firstname: 1,
                                        lastname: 1,
                                        vehicle_num: 1,
                                        vehicle_type: 1,
                                        driving_license_num: 1,
                                        status: 1
                                    }
                     };
  
    const user = await db.collection(col)
                        .findOne(query, projection)
                        .catch(err => {
                            return getUserResponse(400, 'Error in finding the user');
                        });
   
    return getUserResponse(200, user);
};

function getUserResponse(code, data) {
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
