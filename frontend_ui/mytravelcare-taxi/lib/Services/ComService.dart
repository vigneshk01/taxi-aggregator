import 'package:google_maps/google_maps.dart';
import 'package:my_travel_taxi/Models/PsngUser.dart';
import 'package:my_travel_taxi/Models/Ride.dart';
import 'package:my_travel_taxi/Models/StageEnum.dart';
import 'package:my_travel_taxi/Models/TaxiUser.dart';
import 'package:rxdart/rxdart.dart';

class ComService {

  static final BehaviorSubject<LatLng> startLatLng =
        BehaviorSubject<LatLng>.seeded(LatLng(12.9763654,77.5907208));

  static final BehaviorSubject<LatLng> destLatLng =
      BehaviorSubject<LatLng>.seeded(LatLng(12.9846009,77.5950944));

  static final BehaviorSubject<LatLng> rideLatLng =
  BehaviorSubject<LatLng>.seeded(LatLng(12.9809302, 77.5971314));

  static final BehaviorSubject<String> apiKey =
      BehaviorSubject<String>.seeded('');

  static final BehaviorSubject<String> otp =
  BehaviorSubject<String>.seeded('');

  static final BehaviorSubject<Ride> myRide =
  BehaviorSubject<Ride>.seeded(Ride());

  static final BehaviorSubject<Stage> rideStage =
  BehaviorSubject<Stage>.seeded(Stage.GetARide);

  static final BehaviorSubject<List<dynamic>> nearbyRides =
  BehaviorSubject<List<dynamic>>.seeded([]);

  static final BehaviorSubject<PsngUser> psngUser =
  BehaviorSubject<PsngUser>.seeded(PsngUser());

  static final BehaviorSubject<TaxiUser> taxiUser =
  BehaviorSubject<TaxiUser>.seeded(TaxiUser());

  static final BehaviorSubject<String> userType =
  BehaviorSubject<String>.seeded("Passenger");

  static final BehaviorSubject<bool> isBooked =
  BehaviorSubject<bool>.seeded(false);

  static final BehaviorSubject<List<Map<String, dynamic>>> rideHistory =
  BehaviorSubject<List<Map<String, dynamic>>>.seeded([]);


  static void init() {
    startLatLng.add(LatLng(12.9763654,77.5907208));
    destLatLng.add(LatLng(12.9846009,77.5950944));
    rideLatLng.add(LatLng(12.9809302, 77.5971314));
    apiKey.add('');
    otp.add('');
    Ride thisRide = myRide.value;
    thisRide.init();
    myRide.add(thisRide);
    PsngUser thisPsngUser = psngUser.value;
    thisPsngUser.init();
    psngUser.add(thisPsngUser);
    TaxiUser thisTaxiUser = taxiUser.value;
    thisTaxiUser.init();
    taxiUser.add(thisTaxiUser);
    rideStage.add(Stage.GetARide);
    nearbyRides.add([]);
    userType.add("Passenger");
    isBooked.add(false);
    rideHistory.add([]);
  }

  static void dispose() {
    startLatLng.close();
    destLatLng.close();
    rideLatLng.close();
    apiKey.close();
    otp.close();
    myRide.close();
    rideStage.close();
    nearbyRides.close();
    psngUser.close();
    taxiUser.close();
    userType.close();
    isBooked.close();
    rideHistory.close();
  }
}
