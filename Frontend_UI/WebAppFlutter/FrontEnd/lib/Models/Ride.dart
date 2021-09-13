
import 'package:google_maps/google_maps.dart';
import 'package:my_travel_taxi/Services/ComService.dart';

class Ride {
  String? startAddress ;
  String? destAddress;
  LatLng? startLatLng;
  LatLng? destLatLng;
  DateTime? bookedTime;
  DateTime? scheduledTime;
  DateTime? startTime;
  DateTime? endTime;
  String? driverFirstName;
  String? driverLastName;
  String? vehicleType;
  String? vehicleNum;
  String? cost;
  String? passengerRating;
  String? passengerComments;

  initRide() {
    startAddress = null;
    destAddress = null;
    startLatLng = null;
    destLatLng = null;
    bookedTime = null;
    scheduledTime = null;
    startTime = null;
    endTime = null;
    driverFirstName = null;
    driverLastName = null;
    vehicleType = null;
    vehicleNum = null;
    cost = null;
    passengerRating = null;
    passengerComments = null;
  }

  setFromJSON(Map<String, dynamic> body) {
    driverFirstName = body['firstname'];
    driverLastName = body['lastname'];
    vehicleNum = body['vehicle_num'];
    vehicleType = body['vehicle_type'];
    cost = body['cost'];
    ComService.rideLatLng.add(LatLng(body['location']['coordinates'][0],
        body['location']['coordinates'][1]));
  }
}