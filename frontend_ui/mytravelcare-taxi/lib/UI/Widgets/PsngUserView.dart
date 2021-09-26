import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:my_travel_taxi/Services/ComService.dart';

class PsngUserView extends StatefulWidget {
  @override
  _PsngUserState createState() => _PsngUserState();
}

class _PsngUserState extends State<PsngUserView> {
  @override
  Widget build(BuildContext context) {
    return Container(
      color: Colors.white,
      width: 300,
      child: SingleChildScrollView(
        child: Column(
          children: [
            Image(image: AssetImage('images/passenger-icon.png'), width: 150),
            Padding(
              padding: EdgeInsets.all(10),
              child: Text("First Name: ", style: TextStyle(color: Colors.pink)),
            ),
            Padding(
              padding: EdgeInsets.only(top: 5, bottom: 10),
              child: Text(ComService.psngUser.value.firstname),
            ),
            Padding(
              padding: EdgeInsets.all(10),
              child: Text("Last Name: ", style: TextStyle(color: Colors.pink)),
            ),
            Padding(
                padding: EdgeInsets.only(top: 5, bottom: 10),
                child: Text(ComService.psngUser.value.lastname)),
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
