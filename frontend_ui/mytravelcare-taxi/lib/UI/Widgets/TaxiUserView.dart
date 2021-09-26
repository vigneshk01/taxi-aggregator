import 'package:flutter/material.dart';
import 'package:my_travel_taxi/Services/ComService.dart';

class TaxiUserView extends StatefulWidget {
  @override
  _TaxiUserState createState() => _TaxiUserState();
}

class _TaxiUserState extends State<TaxiUserView> {
  @override
  Widget build(BuildContext context) {
    return Container(
      color: Colors.white,
      width: 300,
      child: SingleChildScrollView(
        child: Column(
          children: [
            Image(image: AssetImage('images/driver-icon.png'), width: 150),
            Padding(
              padding: EdgeInsets.all(10),
              child: Text("First Name: ", style: TextStyle(color: Colors.pink)),
            ),
            Padding(
              padding: EdgeInsets.only(top: 5, bottom: 10),
              child: Text(ComService.taxiUser.value.firstname),
            ),
            Padding(
              padding: EdgeInsets.all(10),
              child: Text("Last Name: ", style: TextStyle(color: Colors.pink)),
            ),
            Padding(
              padding: EdgeInsets.only(top: 5, bottom: 10),
              child: Text(ComService.taxiUser.value.lastname),
            ),
            Padding(
              padding: EdgeInsets.all(10),
              child: Text("Vehicle Number: ", style: TextStyle(color: Colors.pink)),
            ),
            Padding(
              padding: EdgeInsets.only(top: 5, bottom: 10),
              child: Text(ComService.taxiUser.value.vehicleNum),
            ),
            Padding(
              padding: EdgeInsets.all(10),
              child: Text("Vehicle Type: ", style: TextStyle(color: Colors.pink)),
            ),
            Padding(
              padding: EdgeInsets.only(top: 5, bottom: 10),
              child: Text(ComService.taxiUser.value.vehicleType),
            ),
            Padding(
              padding: EdgeInsets.all(10),
              child: Text("Driving License Number: ", style: TextStyle(color: Colors.pink)),
            ),
            Padding(
              padding: EdgeInsets.only(top: 5, bottom: 10),
              child: Text(ComService.taxiUser.value.drivingLicenseNum),
            ),
            Padding(
              padding: EdgeInsets.all(10),
              child: Text("User Type: ", style: TextStyle(color: Colors.pink)),
            ),
            Padding(
              padding: EdgeInsets.only(top: 5, bottom: 10),
              child: Text(ComService.userType.value),
            ),
          ],
        ),
      ),
    );
  }
}
