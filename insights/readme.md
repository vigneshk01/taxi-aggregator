Density Map Visualization:
-------------------------
DIR insights/generated_stub_data contains the generated stub data
1. insights/generated_stub_data/location_stream.zip will first need to be extracted to get location_stream.json
2. The json files just need to be imported into the mongo database. 

DATABASE:
1. Update (HOST, PORT) or CONNECTION_STRING and also the DB_NAME in insights/database.py as needed. Please make sure that Database DB_NAME exists at the end point.
2. Use either line 16 or 17 at insights/database.py (Comment the other).

If needed to generate new data following are the steps:
1. run: python booking_stub_data_generator.py
2. This will generate stub data with the following parameters (Code has explanation for each parameter):

        ` RIDE_COLLECTION = 'rides'
            BOOKING_COLLECTION = 'booking'
            LOCATION_STREAM_COLLECTION = 'location_stream'
            GENERATE_LOCATION_DATA = 0
            DAILY_PASSENGER_COUNT = 20
            RANDOM_PASSENGER_COUNT = 50
            TAXI_COUNT = 50
            SHIFT_START = 6
            SHIFT_END = 18
            RUSH_HOUR_1 = 3
            RUSH_HOUR_2 = 8
            FAILED_BOOKING_PROB = 10
            SPAM_BOOKING_PROB = 10
            MAX_SPAM_COUNT = 5
            START_DATE = "01-08-2021"
            DAYS_TO_RUN = 31
            TIME_FORMAT = '%Y-%m-%dT%H:%M:%S'
            HIGH_PROB_SRC = 9
            MID_PROB_SRC = 2
            LOW_PROB_SRC = 1
            RANDOM_PROB_SRC = 8
            LOW_LAT_LONG_SRC = [(12.9035, 77.4914), (12.8546, 77.5676)]
            MID_LAT_LONG_SRC = [(12.9872, 77.5197), (13.1002, 77.5995), (13.0276, 77.6339)]
            HIGH_LAT_LONG_SRC = [(12.9976, 77.6129), (12.9212, 77.6203), (12.9619, 77.5990)]
            HIGH_PROB_DEST = 9
            MID_PROB_DEST = 2
            LOW_PROB_DEST = 1
            RANDOM_PROB_DEST = 8
            LOW_LAT_LONG_DEST = [(12.9035, 77.4914), (12.8546, 77.5676)]
            MID_LAT_LONG_DEST = [(12.9872, 77.5197), (13.1002, 77.5995), (13.0276, 77.6339)]
            HIGH_LAT_LONG_DEST = [(12.9976, 77.6129), (12.9212, 77.6203), (12.9619, 77.5990)]
            SPECIAL_LAT_LONG = (12.9564, 77.7005)
            SPECIAL_DAY = 7
            SPECIAL_HOUR_1 = 0 
            SPECIAL_HOUR_2 = 11
            SPECIAL_BOOKING_COUNT = 20
            BANGALORE_BOUNDARY_JSON = 'db_structure_and_data/map_data/bengaluru_simple_polygon.geojson.json' `

3. If GENERATE_LOCATION_DATA is set to 1, then make sure that the openrouteservice local server is running.
       Steps for setting up openrouteservice local server is found at insights/other/openrouteservice_local_installation

* insights/rides_insights.py is used to get location based insights from booking and ride collections. It will generate 3 maps in separate html files: 
            1. all booking data
            2. failed booking data
            3. all rides data

* insights/rides_insights.py has the following parameters:
   ``` RIDE_COLLECTION = 'rides'
    BOOKING_COLLECTION = 'booking'
    LOCATION_STREAM_COLLECTION = 'location_stream'
    USE_LOCATION = 1
    FROM_DATE = '2021-08-01T00:00:00.000'
    TO_DATE = '2021-08-31T23:59:59.000' ```

* generated outputs are saved at insights/generated_output
* insights/database.py insights/rides.py are not directly used but used by other files.
* insights/location_stream_stub_data.py is used if you want to generate location_stream data based on ride collection separately 
* insights/base_cluster_file_with_interactive_map.ipynb is the ipynb version of insights/rides_insights.py

Feedback Analysis:
-----------------
Dir insights/feedback_sentiment_analysis contains the trained model to classifiy the user feedbacks either as Positive and Negative.
Additional notes are provided under the folder.

Generic Insigts:
---------------
Dir insights/generic_insights contains the basic insights that are created over the arrgregated data in MongoDB, visualized in bar, pie and scatter plots
