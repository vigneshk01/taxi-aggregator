
import 'package:google_maps/google_maps.dart';
import 'package:my_travel_taxi/Data/checker.dart';
import 'package:my_travel_taxi/Services/ComService.dart';

class Ride {
  String startAddress = '' ;
  String destAddress = '';
  LatLng startLatLng = LatLng(0,0);
  LatLng destLatLng = LatLng(0,0);
  String bookedTime = '';
  String scheduledTime = '';
  String startTime = '';
  String endTime = '';
  String driverFirstName = '';
  String driverLastName = '';
  String vehicleType = '';
  String vehicleNum = '';
  String cost = '';
  String passengerRating = '';
  String passengerComments = '';
  String status = '';

  init() {
    startAddress = '';
    destAddress = '';
    startLatLng = LatLng(0,0);
    destLatLng = LatLng(0,0);
    bookedTime = '';
    scheduledTime = '';
    startTime = '';
    endTime = '';
    driverFirstName = '';
    driverLastName = '';
    vehicleType = '';
    vehicleNum = '';
    cost = '';
    passengerRating = '';
    passengerComments = '';
    status = '';
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