# taxi-aggregator-aws

## Location based Taxi Aggregator and Selector

## Introduction

* The Taxi Co-Op wants to build a competing solution to existing cab aggregators while keeping the power in the hands of users and drivers. You’ll help build their backend technology platform.
* You’ll be developing a system to store real-time cab locations, respond to demands from customers based on proximity matches with available drivers. The whole solution should run on AWS.
* You are expected to complete at least the basic requirements. You can choose to pick one or more advanced features as well. The exact scope should be defined by your group and then validated by your mentor and the Great Learning team.

## Basic Requirements

* Each setup will run in a specific area, you’ll need to implement for one specific area in this project. You can define the area under service by a lat/long box. Any driver or user outside this can be ignored.
* You’ll also need to build a process to register each new taxi, with a unique taxi id and their type. You can assume 3-4 types like Utility, Deluxe, Luxury. Similarly, a process to register a user with a unique user id.
* Each taxi will transmit its location (lat/long coordinates) periodically (at least once per minute). You can simulate random initial locations for each taxi in one process on the server-side itself for demonstration purposes. After that, each taxi can be simulated to stay still or move slowly. All this can be done on an EC2 machine.
* Your system should be able to ingest and store these location updates in a scalable way. You can use IoT Core or direct ingestion via an API, to store the data in a geo-aware database, for example, managed MongoDB or DocumentDB
* Each user can make a request for a taxi at any time. They should be able to specify a taxi type preference including ‘All’. You can simulate the users. You can also (optionally) choose to provide APIs for someone to call and raise a request.
* You’ll need to respond to a user’s request with a limited list of closest taxis that match the requested taxi type. While you can do the proximity matching using logic in your application code, the easier and preferable option is to use geospatial features in the database to automatically find relevant taxis.
* The basic requirements don’t involve actual fulfillment of the request and storing information related to that. Just responding to customer requests appropriately is enough.
* The simulator code for taxis and users should be completely independent of the actual server code ingesting data and responding to requests.

The features and systems essential for the system to function are:

	1. Taxi and user registration support and storage with unique ids
	2. Initial area boundary creation and storage
	3. Taxi simulator code with at least 50 taxis
	4. User simulator code for requests demonstrated with at least 5 different users
	5. Ability to ingest taxi location information and user requests in a scalable way:
		* EC2 or AWS IoT Core or API Gateway/Lambda based API, for taxi location update ingestion
		* EC2 or API Gateway/Lambda based APIs for taking in user requests and responding to them
		* This should account for:
			1. A large volume of customer requests (such as a rush hour)
			2. A large migration of available taxis to some locations (rush hour, special events, etc.)
			3. A large number of new taxis becoming available for service (shift change)
	6. Geo-aware database choice, examples - MongoDB, DocumentDB
	7. Service area validation and proximity search in application logic or (preferably) by geo-aware database storage and queries

## Advanced Features
Extend the project further for fulfillment. This would include:

	* Sending notifications to the selected taxis and selection based on first response
	* Sending notification to the user with the selected taxi details
	* API for trip start and end from the taxi
	* Marking the taxi unavailable for other requests during the trip
	* Real-time visualization: The app can show a map location-based view of the supply and demand density. This can be constantly updated based on new location information.
	* All this information aggregated over the long-term can help plan for growth and can even be used by the city planning department for better road and traffic infrastructure planning, based on various insights and patterns. You can process and analyze the information to generate multiple important data points:
	* Taxi traffic density patterns based on hour and day
	* Common high-density area locations
	* User demand patterns based on hour and day
	* Any other relevant analytics
	* With all the available information in real-time and long-term, you can create an innovative approach to spread taxis across the city based on the current and historical density of demand patterns. The app can send hints to drivers to shift their locations to a target area if they are in low-demand areas, and so on.
