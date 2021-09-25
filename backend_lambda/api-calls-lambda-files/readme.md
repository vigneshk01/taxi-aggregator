# MyTravelCare/taxi Backend API AWS Lambdas

### File structure:
1. alltaxis - > lambda returns details of all taxis. It is used by taxi simulator to simulate the fee movement of taxi when not 'Boooked'.
2. api - > Collection of lambdas used by front end to run the app
3. informtaxi - > lambda gets triggered from SNS message sent from 'confirmride' api call. It simulates act of infomaing taxi during ride cofirmation.
4. simulatetaximovement - > lambda gets tiggered from SNS mesage being sent from 'informtaxi' or 'startride'. It uses Google Directions API and the start and end location from SNS message to get the intermediate steps latitude/longitude locations to simulate movement of taxi towards passenger and then from passenger start to end location. It then updates the vehicle location in database.    
