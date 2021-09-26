import 'package:flutter/material.dart';
import 'package:my_travel_taxi/UI/Widgets/NewTaxi.dart';
import 'package:my_travel_taxi/UI/Widgets/NewPassenger.dart';

class SignUp extends StatefulWidget {
  const SignUp({Key? key}) : super(key: key);
  @override
  _SignUpState createState() => _SignUpState();
}

class _SignUpState extends State<SignUp> {
  @override
  Widget build(BuildContext context) {
    return WillPopScope(
      onWillPop: () async => true,
      child: DefaultTabController(
        initialIndex: 2,
        length: 4,
        child: Scaffold(
          appBar: AppBar(
            title: Text("SignUp"),
            centerTitle: true,
            bottom: TabBar(
              tabs: [
                Tab(
                  text: '',
                ),
                Tab(
                  text: 'Taxi',
                ),
                Tab(
                  text: 'Passenger',
                ),
                Tab(text: '')
              ],
            ),
          ),
          body: TabBarView(
            children: [
              Container(
                child: Center(
                  child: Text(
                      'Who are you?\n Taxi service provider or Passenger?\n Choose >'),
                ),
              ),
              NewTaxi(),
              NewPassenger(),
              Container(
                child: Center(
                  child: Text(
                      'Who are you?\n Taxi service provider or Passenger?\n < Choose '),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
