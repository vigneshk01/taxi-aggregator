import 'dart:convert';

import 'package:crypto/crypto.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:google_maps/google_maps.dart' as gmaps;
import 'package:http/http.dart';
import 'package:my_travel_taxi/Data/checker.dart';
import 'package:my_travel_taxi/Models/PathsEnum.dart';
import 'package:my_travel_taxi/Models/Ride.dart';
import 'package:my_travel_taxi/Models/StageEnum.dart';
import 'package:my_travel_taxi/Services/ComService.dart';
import 'package:my_travel_taxi/Services/DataService.dart';
import 'package:my_travel_taxi/Services/MessageService.dart';

class ConfirmRide extends StatefulWidget {
  @override
  _ConfirmRideState createState() => _ConfirmRideState();
}

class _ConfirmRideState extends State<ConfirmRide> {
  late Ride _myRide;
  late bool _onCofirmRidePending;

  @override
  void initState() {
    super.initState();
    _myRide = ComService.myRide.value;
    _onCofirmRidePending = false;
  }

  @override
  Widget build(BuildContext context) {
    return Stack(children: [
      SingleChildScrollView(
        child: Container(
          color: Colors.white,
          width: 300,
          child: Column(
            mainAxisAlignment: MainAxisAlignment.start,
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              Container(
                width: 300,
                color: Colors.pink,
                child: Padding(
                  padding: EdgeInsets.all(20),
                  child: Text(
                    'Confirm Ride Details',
                    style: TextStyle(color: Colors.white, fontSize: 22),
                  ),
                ),
              ),
              Padding(
                padding: EdgeInsets.fromLTRB(14, 20, 20, 5),
                child: Text(
                  'From:',
                  style: TextStyle(fontSize: 14),
                ),
              ),
              Padding(
                padding: EdgeInsets.fromLTRB(14, 0, 20, 5),
                child: Text(
                  _myRide.startAddress!,
                  style: TextStyle(color: Colors.blue, fontSize: 14),
                ),
              ),
              Padding(
                padding: EdgeInsets.fromLTRB(14, 20, 20, 5),
                child: Text(
                  'To:',
                  style: TextStyle(fontSize: 14),
                ),
              ),
              Padding(
                padding: EdgeInsets.fromLTRB(14, 0, 20, 5),
                child: Text(
                  _myRide.destAddress!,
                  style: TextStyle(color: Colors.purple, fontSize: 14),
                ),
              ),
              Padding(
                padding: EdgeInsets.fromLTRB(14, 20, 20, 5),
                child: Text(
                  'Vehicle Number:',
                  style: TextStyle(fontSize: 14),
                ),
              ),
              Padding(
                padding: EdgeInsets.fromLTRB(14, 0, 20, 5),
                child: Text(
                  _myRide.vehicleNum!,
                  style: TextStyle(color: Colors.deepOrange, fontSize: 14),
                ),
              ),
              Padding(
                padding: EdgeInsets.fromLTRB(14, 20, 20, 5),
                child: Text(
                  'Vehicle Type:',
                  style: TextStyle(fontSize: 14),
                ),
              ),
              Padding(
                padding: EdgeInsets.fromLTRB(14, 0, 20, 5),
                child: Text(
                  _myRide.vehicleType!,
                  style: TextStyle(color: Colors.pink, fontSize: 14),
                ),
              ),
              Padding(
                padding: EdgeInsets.fromLTRB(14, 20, 20, 5),
                child: Text(
                  'Scheduled Time:',
                  style: TextStyle(fontSize: 14),
                ),
              ),
              Padding(
                padding: EdgeInsets.fromLTRB(14, 0, 20, 5),
                child: Text(
                  _myRide.scheduledTime!.toString(),
                  style: TextStyle(color: Colors.cyan, fontSize: 14),
                ),
              ),
              Padding(
                padding: EdgeInsets.fromLTRB(14, 20, 20, 5),
                child: Text(
                  'Cost:',
                  style: TextStyle(fontSize: 14),
                ),
              ),
              Padding(
                padding: EdgeInsets.fromLTRB(14, 0, 20, 5),
                child: Text(
                  _myRide.cost!,
                  style: TextStyle(color: Colors.green, fontSize: 14),
                ),
              ),
              Padding(
                padding: EdgeInsets.all(20),
                child: ElevatedButton(
                  onPressed: () {
                    setState(() {
                      _onCofirmRidePending = true;
                    });
                    _onConfirmRidePressed().then((response) {
                      setState(() {
                        _onCofirmRidePending = false;
                      });
                      if (response.statusCode == 200) {
                        final Map<String, dynamic> body = json.decode(response.body);
                        ComService.otp.add(body['OTP'].toString());
                        ComService.rideStage.add(Stage.StartRide);
                        MessageService.showMessage(
                            context, "Confirm Ride Successful!", Colors.green);
                      } else {
                        MessageService.showMessage(
                            context, "Confirm Ride Failed!", Colors.red);
                      }
                    }, onError: (_) {
                      MessageService.showMessage(
                          context, "Confirm Ride Failed!", Colors.red);
                    });
                  },
                  child: Text('Confirm Ride'),
                ),
              ),
            ],
          ),
        ),
      ),
      Visibility(
        visible: _onCofirmRidePending,
        child: LinearProgressIndicator(),
      )
    ]);
  }

  Future<Response> _onConfirmRidePressed() {
    Map<String, dynamic> data = {
      "apiKey": ComService.apiKey.value,
      "startAddress": _myRide.startAddress,
      "destAddress": _myRide.destAddress,
      "startLat": _myRide.startLatLng!.lat,
      "startLng": _myRide.startLatLng!.lng,
      "destLat": _myRide.destLatLng!.lat,
      "destLng": _myRide.destLatLng!.lng,
      "bookedTime": DateTime.now().toIso8601String(),
      "scheduledTime": _myRide.scheduledTime!.toIso8601String(),
      "vehicleType": _myRide.vehicleType,
      "vehicleNum": _myRide.vehicleNum,
    };

    return DataService()
        .postReq(JsonEncoder().convert(data), APIPaths.ConfirmRide.index);
  }
}
