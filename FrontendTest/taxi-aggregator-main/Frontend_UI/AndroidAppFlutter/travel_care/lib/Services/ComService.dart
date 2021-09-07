import 'package:rxdart/rxdart.dart';

class ComService{
  static final BehaviorSubject<double> startLat = BehaviorSubject<double>.seeded(12.9788427);
  static final BehaviorSubject<double> startLong = BehaviorSubject<double>.seeded(77.5974611);
  static final BehaviorSubject<double> destLat = BehaviorSubject<double>.seeded(12.9788027);
  static final BehaviorSubject<double> destLong = BehaviorSubject<double>.seeded(77.5976211);

  static void setStartLat(double newVal) {
    startLat.add(newVal);
  }

  static void setStartLong(double newVal) {
    startLong.add(newVal);
  }

  static void setDestLat(double newVal) {
    destLat.add(newVal);
  }

  static void setDestLong(double newVal) {
    destLong.add(newVal);
  }

  static double getStartLat(double newVal) {
    return startLat.value;
  }

  static double getStartLong(double newVal) {
    return startLong.value;
  }

  static double getDestLat(double newVal) {
    return destLat.value;
  }

  static double getDestLong(double newVal) {
    return destLong.value;
  }


  static void dispose() {
    startLat.close();
    startLong.close();
    destLat.close();
    destLong.close();
  }
}