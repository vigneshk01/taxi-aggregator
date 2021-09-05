import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:my_travel_taxi/Models/StageEnum.dart';
import 'package:my_travel_taxi/Services/ComService.dart';
import 'package:my_travel_taxi/UI/Widgets/ConfirmRide.dart';
import 'package:my_travel_taxi/UI/Widgets/EndRide.dart';
import 'package:my_travel_taxi/UI/Widgets/GetRide.dart';
import 'package:my_travel_taxi/UI/Widgets/MapView.dart';
import 'package:my_travel_taxi/UI/Widgets/RideFeedback.dart';
import 'package:my_travel_taxi/UI/Widgets/StartRide.dart';

class RouteView extends StatefulWidget {
  @override
  _RouteViewState createState() => _RouteViewState();
}

class _RouteViewState extends State<RouteView> {
  final GlobalKey<ScaffoldState> _scaffoldKey = new GlobalKey<ScaffoldState>();

  late Stage _rideStage;

  @override
  void initState() {
    super.initState();
    _rideStage = ComService.rideStage.value;

    ComService.rideStage.listen((value) {
      setState(() {
        _rideStage = value;
      });
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("Set Route"),
        centerTitle: true,
      ),
      //drawer: getDrawer(),
      //body: MapView(),
      body: Flex(
        direction: Axis.horizontal,
        children: [
          getDrawer(),
          Expanded(
            flex: 4,
            child: MapView(),
          ),
        ],
      ),
    );
  }

  Widget getDrawer() {
    switch (_rideStage) {
      case Stage.GetARide:
        return GetRide();
      case Stage.ConfirmRide:
        return ConfirmRide();
      case Stage.StartRide:
        return StartRide();
      case Stage.EndRide:
        return EndRide();
      case Stage.FeedbackOnRide:
        return RideFeedback();
      default:
        return GetRide();
    }
  }
}
