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

class StartRide extends StatefulWidget {
  @override
  _StartRideState createState() => _StartRideState();
}

class _StartRideState extends State<StartRide> {
  late Ride _myRide;
  late bool _onStartRidePending;
  late String _otpVal;

  @override
  void initState() {
    super.initState();
    _myRide = ComService.myRide.value;
    _onStartRidePending = false;
    _otpVal = ComService.otp.value;
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
                    'Starting Ride...',
                    style: TextStyle(color: Colors.white, fontSize: 22),
                  ),
                ),
              ),
              Padding(
                padding: EdgeInsets.fromLTRB(14, 20, 20, 5),
                child: Text(
                  'Driver:',
                  style: TextStyle(fontSize: 14),
                ),
              ),
              Padding(
                padding: EdgeInsets.fromLTRB(14, 0, 20, 5),
                child: Text(
                  _myRide.driverFirstName! +
                      ' ' +
                      _myRide.driverLastName!,
                  style: TextStyle(color: Colors.blue, fontSize: 14),
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
                padding: EdgeInsets.all(20),
                child: Container(
                  width: 150,
                  child: TextFormField(
                    readOnly: true,
                    initialValue: ComService.otp.value,
                    textAlign: TextAlign.center,
                    decoration: InputDecoration(
                      hintText: "OTP",
                      filled: true,
                      fillColor: Colors.white,
                    ),
                    validator: (value) {
                      if (value == null || value.isEmpty) {
                        return 'Please enter password';
                      }
                      else if(value.length == 0 || value.length > 6) {
                        return 'OTP should be 6 digits only';
                      }
                      else if(value.contains(RegExp(r'[0-9]')) == false){
                        return 'OTP is a 6 digit number';
                      }
                      return null;
                    },
                  ),
                ),
              ),
              Padding(
                padding: EdgeInsets.all(20),
                child: ElevatedButton(
                  onPressed: () {
                    setState(() {
                      _onStartRidePending = true;
                    });
                    _onStartRidePressed().then((response) {
                      setState(() {
                        _onStartRidePending = false;
                      });
                      if (response.statusCode == 200) {
                        final Map<String, dynamic> body = json.decode(response.body);
                        _myRide.startTime = DateTime.parse(body['start_time']);
                        ComService.myRide.add(_myRide);
                        ComService.rideStage.add(Stage.EndRide);
                        MessageService.showMessage(
                            context, "Ride Started Successful!", Colors.green);
                      } else {
                        MessageService.showMessage(
                            context, "Failed to Start Ride!", Colors.red);
                      }
                    }, onError: (_) {
                      MessageService.showMessage(
                          context, "Failed to Start Ride!", Colors.red);
                    });
                  },
                  child: Text('Start Ride'),
                ),
              ),
            ],
          ),
        ),
      ),
      Visibility(
        visible: _onStartRidePending,
        child: LinearProgressIndicator(),
      )
    ]);
  }

  Future<Response> _onStartRidePressed() {
    Map<String, dynamic> data = {
      "updateType": "startTime",
      "apiKey": ComService.apiKey.value,
      "OTP": sha256.convert(_otpVal.codeUnits).toString(),
      "startTime": DateTime.now().toIso8601String()
    };

    return DataService()
        .postReq(JsonEncoder().convert(data), APIPaths.UpdateRide.index);
  }
}
