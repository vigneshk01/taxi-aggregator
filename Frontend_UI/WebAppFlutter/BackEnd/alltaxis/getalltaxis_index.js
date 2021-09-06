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
                                return getTaxisResponse(400, 'Error in connecting to db');
                            });
                            
      if (client) {
        // Specify which database we want to use
        const db = await client.db(process.env.MONGODB_DB);
        cachedDb = db;
        return db;    
      }
      else {
          return getTaxisResponse(400, 'Error in connecting to db');
      }
      
}

exports.handler = async (event) => {
    
    // Get an instance of our database
    const db = await connectToDatabase();
    
    let query = {};
    
    let projection = {
                        projection: {
                                        _id: 0,
                                    }
                     };
  
    const taxisList = await db.collection(process.env.COL_TAXI)
                        .find(query, projection)
                        .toArray()
                        .catch(() => {
                            return getTaxisResponse(400, 'Error in finding the t');
                        });
   
    return getTaxisResponse(200, taxisList);
};

function getTaxisResponse(code, data) {
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
