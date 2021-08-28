import 'package:travel_care/Models/User.dart';

class Driver implements User {
  @override
  String? firstName;

  @override
  String? lastName;

  @override
  String? password;

  @override
  String? username;

  String? vehicleNumber;
  String? licenseNumber;
}
