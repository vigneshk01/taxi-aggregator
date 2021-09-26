class TaxiUser {
  String firstname = '';
  String lastname = '';
  String vehicleType = '';
  String vehicleNum = '';
  String drivingLicenseNum = '';
  String status = '';

  init() {
    firstname = '';
    lastname = '';
    vehicleType = '';
    vehicleNum = '';
    drivingLicenseNum = '';
    status = '';
  }

  setFromJSON(Map<String, dynamic> body) {
    firstname = body['firstname'];
    lastname = body['lastname'];
    vehicleType = body['vehicle_type'];
    vehicleNum = body['vehicle_num'];
    drivingLicenseNum = body['driving_license_num'];
    status = body['status'];
  }
}