import 'package:flutter/material.dart';

import '2_Login.dart';

class SplashScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Material(
      child: InkWell(
        child: Center(
          child: Text(
            "TravelCare.taxicabs",
            style: TextStyle(
              fontSize: 36,
              color: Colors.pink,
            ),
          ),
        ),
        onTap: () {
          Navigator.push(context, MaterialPageRoute(builder: (context) {
            return Login();
          }));
        },
      ),
    );
  }
}
