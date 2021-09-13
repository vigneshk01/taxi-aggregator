import 'package:google_maps/google_maps.dart';
import 'package:my_travel_taxi/Models/Ride.dart';
import 'package:my_travel_taxi/Models/StageEnum.dart';
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

  static void dispose() {
    startLatLng.close();
    destLatLng.close();
    rideLatLng.close();
    apiKey.close();
    otp.close();
    myRide.close();
    rideStage.close();
  }
}
