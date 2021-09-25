# MyTravelCare/taxi Backedn API AWS Lambdas

### File structure:
1. alltaxis - > lambda returns details of all taxis. It is used by taxi simulator to simulate the fee movement of taxi when not 'Boooked'.
2. api - > Collection of lambdas used by front end to run the app
3. informtaxi - > lambda gets triggered from SNS message sent from 'confirmride' api call. It simulates act of infomaing taxi during ride cofirmation.
4. simulatetaximovement - > lambda gets tiggered from SNS mesage being sent from 'informtaxi' or 'startride'. 
5. It used Googe Directions PAI and the start and end location from SNS message to get the steps latitude and longitude location. 
6. It is then used to update the vehicle location in database.    
