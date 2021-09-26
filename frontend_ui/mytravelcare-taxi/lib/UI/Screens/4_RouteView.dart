import 'dart:async';
import 'dart:convert';

import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:http/http.dart';
import 'package:my_travel_taxi/Models/PathsEnum.dart';
import 'package:my_travel_taxi/Models/PsngUser.dart';
import 'package:my_travel_taxi/Models/StageEnum.dart';
import 'package:my_travel_taxi/Models/TaxiUser.dart';
import 'package:my_travel_taxi/Services/ComService.dart';
import 'package:my_travel_taxi/Services/DataService.dart';
import 'package:my_travel_taxi/Services/MessageService.dart';
import 'package:my_travel_taxi/UI/Screens/5_RideHistory.dart';
import 'package:my_travel_taxi/UI/Widgets/ConfirmRide.dart';
import 'package:my_travel_taxi/UI/Widgets/EndRide.dart';
import 'package:my_travel_taxi/UI/Widgets/GetRide.dart';
import 'package:my_travel_taxi/UI/Widgets/MapView.dart';
import 'package:my_travel_taxi/UI/Widgets/PsngUserView.dart';
import 'package:my_travel_taxi/UI/Widgets/RideFeedback.dart';
import 'package:my_travel_taxi/UI/Widgets/StartRide.dart';
import 'package:my_travel_taxi/UI/Widgets/TaxiUserView.dart';
import 'package:my_travel_taxi/UI/Widgets/ThisTaxi.dart';

class RouteView extends StatefulWidget {
  @override
  _RouteViewState createState() => _RouteViewState();
}

class _RouteViewState extends State<RouteView> {
  late Stage _rideStage;
  late StreamSubscription subsc;
  late String userType;

  @override
  void initState() {
    super.initState();

    userType = ComService.userType.value;

    _rideStage = ComService.rideStage.value;

    subsc = ComService.rideStage.listen((value) {
      if (mounted) {
        setState(() {
          _rideStage = value;
        });
      }
    });
  }

  @override
  void dispose() {
    super.dispose();
    subsc.cancel();
  }

  @override
  Widget build(BuildContext context) {
    return WillPopScope(
      onWillPop: () async => false,
      child: Scaffold(
        appBar: AppBar(
          title: Text("Set Route"),
          centerTitle: true,
          actions: [
            Padding(
              padding: EdgeInsets.only(right: 20),
              child: MouseRegion(
                  cursor: SystemMouseCursors.click,
                  child: GestureDetector(
                    onTap: () {
                      Navigator.push(
                        context,
                        MaterialPageRoute(builder: (context) => RideHistory()),
                      );
                    },
                    child: Icon(
                      Icons.access_time_outlined,
                      color: Colors.redAccent,
                    ),
                  )),
            ),
            Padding(
              padding: EdgeInsets.only(right: 20),
              child: MouseRegion(
                  cursor: SystemMouseCursors.click,
                  child: GestureDetector(
                    onTap: () {
                      ComService.init();
                      Navigator.pop(context);
                    },
                    child: Icon(
                      Icons.power_settings_new_rounded,
                      color: Colors.redAccent,
                    ),
                  )),
            )
          ],
        ),
        drawer: ((userType == "Passenger")
            ? PsngUserView()
            : ((userType == "Taxi") ? TaxiUserView() : Container())),
        onDrawerChanged: (check) {},
        body: Flex(
          direction: Axis.horizontal,
          children: [
            getStateWidget(),
            Expanded(
              flex: 4,
              child: MapView(),
            ),
          ],
        ),
      ),
    );
  }

  Widget getStateWidget() {
    if (ComService.userType.value == "Taxi") {
      ComService.rideStage.add(Stage.ThisTaxi);
      return ThisTaxi();
    } else {
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
}
