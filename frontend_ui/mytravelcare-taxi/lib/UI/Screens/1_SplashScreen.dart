import 'package:flutter/material.dart';
import 'package:my_travel_taxi/Services/ComService.dart';

import '2_Login.dart';

class SplashScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Material(
      child: InkWell(
        child: Center(
          child: Text(
            "myTravelCare/taxi",
            style: TextStyle(
              fontSize: 40,
              color: Colors.pink,
            ),
          ),
        ),
        onTap: () {
          Navigator.push(
            context,
            MaterialPageRoute(builder: (context) => Login()),
          );
        },
      ),
    );
  }
}
