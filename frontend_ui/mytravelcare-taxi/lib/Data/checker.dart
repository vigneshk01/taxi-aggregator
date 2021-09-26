import 'package:google_maps/google_maps.dart';

class Checker {
  static final Map<String, dynamic> checkMap = {

    'apiURI': 'https://fep34ikk65.execute-api.us-east-1.amazonaws.com/dev',

    'mapBounds': LatLngBounds(LatLng(12.7144008,77.2668972),
        LatLng(13.1298197,78.0910555)),

    'mapCenter': LatLng(12.9788427, 77.5974611),

    'endPointsAddressList': [
      'Cubbon Park, Bengaluru, Karnataka, India',
      'Queens Road, Bengaluru, Karnataka, India',
      'Anil Kumble Circle, Bengaluru, Karnataka, India',
      'Vittal Mallya Junction, Bengaluru,Karnataka, India',
      'Museum Road, Bengaluru,Karnataka, India'
    ],

    'endPointsLocList': [
      LatLng(12.9763654,77.5907208),
      LatLng(12.9846009,77.5950944),
      LatLng(12.9765739,77.599608),
      LatLng(12.9703405,77.598533),
      LatLng(12.9722849,77.6020567),
    ],

    'vehicleTypeList': ["UTILITY", "DELUXE", "LUXURY"],

    'scheduleTimeList': ["sometime now", "after 30 mins", "after 1 hour"]
  };
}
