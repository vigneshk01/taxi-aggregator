# /api/rides/*

### Lambdas
1. confirmride - > lambda that creates new ride details in database and sends SNS message to 'informtaxi' to simulate taxi movement towards passenger start location.
2. getaride - > lambda that gets an 'ACTIVE' taxi from database and sets it to 'BOOKED'
3. getridedetails - > lambda that gets details of a particular ride stored in database.
4. getridelocation - > lambda that gets the current vehicle location for that particular ride.
5. updateride - > lambda that updates ride details like start time, end time or feedback details in database.
