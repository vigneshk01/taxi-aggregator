import 'package:flutter/material.dart';
import 'package:travel_care/UI/Widgets/MapView.dart';
import 'package:travel_care/UI/Widgets/RideSelection.dart';

class RouteView extends StatefulWidget {
  @override
  _RouteViewState createState() => _RouteViewState();
}

class _RouteViewState extends State<RouteView> {

  @override
  void initState() {
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Select Transit Route'),
      ),
      drawer: RideSelection(),
      body: MapView(),
    );
  }
}
