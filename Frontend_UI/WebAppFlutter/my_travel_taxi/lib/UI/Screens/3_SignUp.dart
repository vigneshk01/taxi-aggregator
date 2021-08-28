import 'package:flutter/material.dart';
import 'package:my_travel_taxi/UI/Widgets/NewDriver.dart';
import 'package:my_travel_taxi/UI/Widgets/NewPassenger.dart';

class SignUp extends StatefulWidget {
  const SignUp({Key? key}) : super(key: key);
  @override
  _SignUpState createState() => _SignUpState();
}

class _SignUpState extends State<SignUp> {
  @override
  Widget build(BuildContext context) {
    return DefaultTabController(
      length: 2,
      child: Scaffold(
        appBar: AppBar(
          title: Text("SignUp"),
          centerTitle: true,
          bottom: TabBar(
            tabs: [
              Tab(
                child: Text('Driver'),
              ),
              Tab(
                child: Text('Passenger'),
              )
            ],
          ),
        ),
        body: TabBarView(children: [
          NewDriver(),
          NewPassenger(),
        ],),
      ),
    );
  }
}
