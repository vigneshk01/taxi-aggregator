# Location based Taxi Selector and Aggregator

1. The contents are categorized based on their functionalility in each of the sub directory.
2. Further instructions have been provided for deployment and additional configurations under the root of each sub directory.

Directories Overview:
-------------
  1. backend_lambda - provides the lambda side code used for managign the user registration and simulator calls @ the server side. 
  2. db_structure_and_data - contains all the MongoDB collections and its structure , also contains the dump of the DB. 
  3. design_diagrams - provides overview of the product and implementation
  4. frontend_ui - the directory hosts all the frontend code for populating and booking Taxi's from the UI.
  5. insights - provides various data and insights that are genereated over a period by the Taxi APP.
  6. payments - contains the code for the payment interface that will be triggered by the Frontend app.
  7. other - contains mostly additional packages and code that was utlized at various stagess by the app. 
  8. taxi_simulator - the simulator code for randome movement of taxi withib the boundary.
  9. user_simulator - handles the taxi search and cab booking at the console level.
