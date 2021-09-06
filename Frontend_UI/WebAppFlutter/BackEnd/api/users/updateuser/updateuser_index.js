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
                                return updateUserResponse(400, 'Error in connecting to db');
                            });
                            
      if (client) {
        // Specify which database we want to use
        const db = await client.db(process.env.MONGODB_DB);
        cachedDb = db;
        return db;    
      }
      else {
          return updateUserResponse(400, 'Error in connecting to db');
      }
      
}

exports.handler = async (event) => {
    let body = JSON.parse(event.body);
    
    // Get an instance of our database
    const db = await connectToDatabase();
    
    let col = process.env.COL_PSNG;
    if (body.userType == process.env.USER_TYPE_PSNG) {
        //col = process.env.COL_PSNG;
        updateUserResponse(400, "Unsupported user type");
    }
    else if (body.userType == process.env.USER_TYPE_TAXI) {
        col = process.env.COL_TAXI;
    }
    else {
        updateUserResponse(400, "Invalid user type");
    }
    
    let updatefilter = {
                            APIKey: body.apiKey,
                            vehicle_num: body.vehicle_num
                      };
    
    let dt = new Date().toISOString();             
                
    let data = {};
    switch(body.updateType) {
        case "taxiLoc":
            data = {
                        $set: {
                                location: {
                                    type: "Point",
                                    coordinates: [body.lat, body.lng]
                                },
                                last_updated_timestamp: dt,
                                status: body.status
                              }
                   };
            break;
        default:
            return updateUserResponse(400, 'Unsupported update type');
    }
  
    const updateResponse = await db.collection(col)
                        .updateOne(updatefilter, data)
                        .catch(() => {
                            return updateUserResponse(400, "Update Failed!");
                        });
                        
    if (updateResponse.acknowledged) {
        return updateUserResponse(200, "Successful update!");
    }
    else {
        return updateUserResponse(400, "Update Failed!");
    }
};

function updateUserResponse(code, data) {
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