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
                                return nearbyRidesResponse(400, 'Error conecting to the db');
                            });
                            
      if (client) {
        // Specify which database we want to use
        const db = await client.db(process.env.MONGODB_DB);
        cachedDb = db;
        return db;    
      }
      else {
            return nearbyRidesResponse(400, 'Error connecting to the db');
      }
      
}

exports.handler = async (event) => {
    let body = JSON.parse(event.body);
    
    const db = await connectToDatabase();
    
    let query = {
                    location:
                    {
                        $near :
                        {
                            $geometry: { type: "Point",  coordinates: [ body.lat, body.lng ] },
                            $minDistance: 0,
                            $maxDistance: 5000
                        }
                    }
                };
    
    let projection = {
                        projection: {
                                        _id: 0,
                                        vehicle_num: 1,
                                        vehicle_type: 1,
                                        location: 1,
                                    }
                     };
  
    const nearbyRides = await db.collection(process.env.COL_TAXI)
                        .find(query, projection)
                        .toArray()
                        .catch(err => {
                            return nearbyRidesResponse(400, 'Could not find nearby rides');
                        });
   
    return nearbyRidesResponse(200, nearbyRides);
};

function nearbyRidesResponse(code, data) {
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