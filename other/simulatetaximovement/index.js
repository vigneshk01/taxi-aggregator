'use strict';

const {Client} = require("@googlemaps/google-maps-services-js");
const MongoClient = require("mongodb").MongoClient;

exports.handler = async (event) => {
    
    let response = null;
    let client = null;
    
    try {
        // Get the body of event in JSON format
        const body = JSON.parse(event.Records[0].Sns.Message);
        
        console.log(JSON.stringify(event));
        
        // Create a Mongo client
        client = await MongoClient
                                .connect(process.env.MONGODB_URI);
        
        // Connect to the Mongo database
        const db = await client.db(process.env.MONGODB_DB);
        
        // js google maps client
        const mapClient = new Client({});
        
        // directions request data
        let directionsRequest = {
            params: {
                key: process.env.GOOGLE_MAPS_API_KEY,
                origin: body.start_loc,
                destination: body.end_loc,
            }
        };
      
        // Get directions for a particular route
        const directionsResponse = await mapClient.directions(directionsRequest);
        
        console.log(directionsResponse);
        
        // Get the first/only leg of the route
        let pointDets = directionsResponse.data.routes[0].legs[0];
        
        // Get the total distance of route in kms as a string
        let totalDist = pointDets.distance.text;
        // Get the estimates time taken to complete travel while DRIVING
        let estTotalTime = pointDets.duration.text;
        
        // Filter data to get a particular ride detail
        let updatefilter = {
            OTPHash: body.OTPHash,
            vehicle_num: body.vehicle_num,
            status: body.status
        };
        
        // Data to be updated in rides colection in database
        let data = {
            $set: {
                total_distance: totalDist,
                est_time: estTotalTime
            }
        };
        
        // Update the total distance and estimated time for route
        const updTDRes = await db.collection(process.env.COL_RIDES).updateOne(updatefilter, data);
                        
        console.log("1: "+JSON.stringify(updTDRes));
                        
        // for each steps in a leg in the route get coordinates
        for(const step of pointDets.steps) {
            
            console.log(JSON.stringify(step));
            
            data = {
                $set: {
                    current_vehicle_location: {
                        type: "Point",
                        coordinates: [step.end_location.lat, step.end_location.lng]
                    },
                    instruction: step.html_instructions,
                    distance: step.distance.text,
                    duration: step.duration.text
                }
            };
            
            // Create a delay of 7 seconds to enble user to read this data
            // from database
            await sleep(7000);
            
            // Update the step coordiantes in ride's current vehicle location
            const upRes = await db.collection(process.env.COL_RIDES).updateOne(updatefilter, data);
                    
            console.log("2: "+JSON.stringify(upRes));
        }
        
        // On completion response with success message
        response =  simulateTaxiResponse(200, "Taxi movement simulation successful!");
                        
    }
    catch(error) {
        console.log(error);
        if (response == null) {
            response = simulateTaxiResponse(400, "Taxi movement simulation failed!");
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

// Function that when called creates a delay of user defined milliseconds
const sleep = (milliseconds) => {
  return new Promise((resolve) => {
    setTimeout(resolve, milliseconds);
  });
};

// Structure of response
function simulateTaxiResponse(code, data) {
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


