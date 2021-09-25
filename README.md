# Location based Taxi Selector and Aggregator

Summary:
-------
This Application provides Taxi Service in real-time within a given boundary, based on the location aspects and cab availability.
For this implementation, We have fixed Bangalore as our base location for the Taxi Service. The Solution is full and full designed to run on AWS cloud.
Some of the AWS services that it utilizes are Lambda, EC2, API Gateway, Kinesis stream, SageMaker etc 

Notes:
-----
1. The source code contents are categorized based on their functionalility in each of the sub directory.
2. Further instructions have been provided for deployment and additional configurations, under the root of each sub directory.

Directories Overview:
-------------
  1. backend_lambda - contains the lambda-functions used for managing the user registration and simulator calls at the server side. 
  2. db_structure_and_data - contains all the MongoDB collections and its structure for the basic requirement, also contains the dump of the DB. 
  3. design_diagrams - provides overview of the product and the implementation.
  4. frontend_ui - the directory contains all the code for registration and map Interface and support for booking Taxi's from the UI.
  5. insights - code for generation of various statistics that are computed, based on the data genereated over a period of time, by the Taxi APP.
  6. payments - contains the code for the payment interface that will be triggered by the Frontend app.
  7. other - contains mostly additional packages and code that was utlized at various stages by the app. 
  8. taxi_simulator - the simulator code for initial random movement of taxi within the given boundary.
  9. user_simulator - contains code handles the user side activites such as taxi search and cab booking at the console level.
