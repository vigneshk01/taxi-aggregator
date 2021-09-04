const MongoClient = require('mongodb').MongoClient;
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
                                return getARideResponse(400, 'Error in connecting to db');
                            });
                            
      if (client) {
        // Specify which database we want to use
        const db = await client.db(process.env.MONGODB_DB);
        cachedDb = db;
        return db;    
      }
      else {
          return getARideResponse(400, 'Error in connecting to db');
      }
      
}

exports.handler = async (event) => {
    
    let body = JSON.parse(event.body);
    
    // Get an instance of our database
    const db = await connectToDatabase();
    
    let col = process.env.COL_TAXI;
    
    /*let dt = new Date();
    dt.setHours(dt.getMinutes() - 30 );*/
    /*last_updated_timestamp: { // 30 minutes ago (from now)
                        $gt: dt.toISOString()
                    },*/
                    
    let start_loc = { latitude: body.startLat, longitude: body.startLng };
    let end_loc = { latitude: body.destLat, longitude: body.destLng };
    
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
            return getARideResponse(400, 'Invalid vehicle type');
    }
    
    cost = cost.toFixed(2);
    
    let query = {
                    location:
                    { $near :
                        {
                            $geometry: { type: "Point",  coordinates: [body.startLat, body.startLng] },
                            $minDistance: 0,
                            $maxDistance: 5000
                        }
                    },
                    vehicle_type: body.vehicle_type,
                    status: "ACTIVE"
                };
                
    let projection = { 
                        projection: {
                                        _id: 0, 
                                        firstname: 1, 
                                        lastname: 1,
                                        vehicle_num: 1, 
                                        vehicle_type: 1, 
                                        location: 1
                                    }
                     };
                     
    let ride = await db.collection(col)
                         .findOne(query, projection)
                         .catch(() => {
                                        return getARideResponse(400, 'Could not find a ride');
                         });
    
    ride["cost"] = cost;

    return getARideResponse(200, ride);
};

function getARideResponse(code, data) {
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
