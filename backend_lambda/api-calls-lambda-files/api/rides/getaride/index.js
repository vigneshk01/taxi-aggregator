const MongoClient = require('mongodb').MongoClient;
const haversine = require('haversine');

exports.handler = async (event) => {
    
    let response = null;
    let client = null;
    
    try {
        // Get the body of event in JSON format
        const body = JSON.parse(event.body);
        
        console.log(event);
        
        // Create a Mongo client
        client = await MongoClient
                                .connect(process.env.MONGODB_URI);
        
        // Connect to the Mongo database
        const db = await client.db(process.env.MONGODB_DB);
    
        // Get Taxi collection name
        let col = process.env.COL_TAXI;

        // Structure of start and end location for haversine distancee calculation                        
        let start_loc = { latitude: body.start_lat, longitude: body.start_lng };
        let end_loc = { latitude: body.dest_lat, longitude: body.dest_lng };
        
        const distance = haversine(start_loc, end_loc);
        
        // Cost calculation using distance
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
                response = getARideResponse(400, {message: "Invalid vehicle type"});
        }
        // Fix cost value to two decimal places
        cost = cost.toFixed(2);
        
        // Filter data structure
        let query = {
            location: {
                $near : {
                    $geometry: { type: "Point",  coordinates: [body.start_lat, body.start_lng] },
                    $minDistance: 0,
                    $maxDistance: 5000
                }
            },
            vehicle_type: body.vehicle_type,
            status: "ACTIVE"
        };
        
        // Update data for taxi status            
            let updStatusData = {
                $set: {
                    status: "BOOKED"
                }
            };
                    
        // Structure of data to returnfrom database                    
        let projection = { 
            projection: {
                _id: 0, 
                firstname: 1, 
                lastname: 1,
                vehicle_num: 1, 
                vehicle_type: 1, 
                location: 1
            },
            returnOriginal: false
        };
        
        // Get ride details from database                 
        let ride = await db.collection(col).findOneAndUpdate(query, updStatusData, projection);
        
        console.log(JSON.stringify(ride));
        
        // If success then return ride else return failure response
        if (ride["value"]) {
            
            // Add calculated cost to ride data
            ride["value"]["cost"] = cost;
            
            response = getARideResponse(200, ride["value"]);
        }
        else {
            response= getARideResponse(400, {message: "Failed to get ride!"});
        }
    }
    catch(error) {
        console.log(error);
        if (response == null) {
            response = getARideResponse(400, {message: "Failed to get ride!"});
        }
    }
    finally {
        // Close mongo client
        if (client) {
            await client.close();
        }
        return response;
    }
};

// Structure of response
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
