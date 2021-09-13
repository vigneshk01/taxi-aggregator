import 'package:flutter/material.dart';
import 'package:my_travel_taxi/UI/Screens/1_SplashScreen.dart';
import 'package:my_travel_taxi/UI/Screens/3_SignUp.dart';
import 'package:my_travel_taxi/UI/Screens/4_RouteView.dart';

import 'UI/Screens/2_Login.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'myTravel_Taxi',
      theme: ThemeData(
        primarySwatch: Colors.pink,
        primaryTextTheme: TextTheme(
            headline6: TextStyle(
          color: Colors.pink,
          fontSize: 24,
        )),
        primaryIconTheme: IconThemeData(
          color: Colors.pink,
        ),
        appBarTheme: AppBarTheme(
          backgroundColor: Colors.transparent,
          elevation: 0.0,
        ),
        tabBarTheme: TabBarTheme(labelColor: Colors.pink),
      ),
      initialRoute: '/',
      routes: {
        '/': (context) => SplashScreen(),
        '/login': (context) => Login(),
        '/signup': (context) => SignUp(),
        '/routeview': (context) => RouteView(),
      },
    );
  }
}
