import 'dart:convert';

import 'package:crypto/crypto.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:google_maps/google_maps.dart' as gmaps;
import 'package:http/http.dart';
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
      Container(
        height: double.infinity,
        child: SingleChildScrollView(
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
                    style: TextStyle(color: Colors.pink, fontSize: 14),
                  ),
                ),
                Padding(
                  padding: EdgeInsets.fromLTRB(14, 0, 20, 5),
                  child: Text(
                    _myRide.driverFirstName + ' ' + _myRide.driverLastName,
                    style: TextStyle(fontSize: 14),
                  ),
                ),
                Padding(
                  padding: EdgeInsets.fromLTRB(14, 20, 20, 5),
                  child: Text(
                    'Vehicle Number:',
                    style: TextStyle(color: Colors.pink, fontSize: 14),
                  ),
                ),
                Padding(
                  padding: EdgeInsets.fromLTRB(14, 0, 20, 5),
                  child: Text(
                    _myRide.vehicleNum,
                    style: TextStyle(fontSize: 14),
                  ),
                ),
                Padding(
                  padding: EdgeInsets.fromLTRB(14, 20, 20, 5),
                  child: Text(
                    'Vehicle Type:',
                    style: TextStyle(color: Colors.pink, fontSize: 14),
                  ),
                ),
                Padding(
                  padding: EdgeInsets.fromLTRB(14, 0, 20, 5),
                  child: Text(
                    _myRide.vehicleType,
                    style: TextStyle(fontSize: 14),
                  ),
                ),
                Padding(
                  padding: EdgeInsets.fromLTRB(14, 20, 20, 5),
                  child: Text(
                    'OTP:',
                    style: TextStyle(color: Colors.pink, fontSize: 14),
                  ),
                ),
                Padding(
                  padding: EdgeInsets.fromLTRB(14, 0, 20, 5),
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
                        } else if (value.length == 0 || value.length > 6) {
                          return 'OTP should be 6 digits only';
                        } else if (value.contains(RegExp(r'[0-9]')) == false) {
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
                      if (mounted) {
                        setState(() {
                          _onStartRidePending = true;
                        });
                      }
                      _onStartRidePressed().then((response) {
                        if (mounted) {
                          setState(() {
                            _onStartRidePending = false;
                          });
                        }
                        if (response.statusCode == 200) {
                          final Map<String, dynamic> body =
                              json.decode(response.body);
                          _myRide.startTime =
                              body['start_time'];
                          ComService.myRide.add(_myRide);
                          ComService.rideStage.add(Stage.EndRide);
                          MessageService.showMessage(context,
                              "Ride Started Successful!", Colors.green);
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
                Padding(
                  padding: EdgeInsets.all(20),
                  child: ElevatedButton(
                    onPressed: () {
                      if (mounted) {
                        setState(() {
                          _onStartRidePending = true;
                        });
                      }
                      _onRefreshRideLocationPressed().then((response) {
                        if (mounted) {
                          setState(() {
                            _onStartRidePending = false;
                          });
                        }
                        if (response.statusCode == 200) {
                          final Map<String, dynamic> _rideLoc =
                              json.decode(response.body);
                          ComService.rideLatLng.add(gmaps.LatLng(
                              _rideLoc['current_vehicle_location']
                                  ['coordinates'][0],
                              _rideLoc['current_vehicle_location']
                                  ['coordinates'][1]));
                          MessageService.showMessage(
                              context, "Ride location updated!", Colors.green);
                        } else {
                          MessageService.showMessage(context,
                              "Failed to show ride location!", Colors.red);
                        }
                      }, onError: (err) {
                        if (mounted) {
                          setState(() {
                            _onStartRidePending = false;
                          });
                        }
                        MessageService.showMessage(context,
                            "Failed to show ride location!", Colors.red);
                      });
                    },
                    child: Text('Refresh Ride Location'),
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
      Visibility(
        visible: _onStartRidePending,
        child: Container(
          width: 300,
          child: LinearProgressIndicator(
            color: Colors.yellow,
          ),
        ),
      )
    ]);
  }

  Future<Response> _onStartRidePressed() {
    Map<String, dynamic> data = {
      "update_type": "startTime",
      "apiKey": ComService.apiKey.value,
      "OTPHash": sha256.convert(_otpVal.codeUnits).toString(),
      "start_time": DateTime.now().toIso8601String(),
      "start_lat": _myRide.startLatLng.lat,
      "start_lng": _myRide.startLatLng.lng,
      "dest_lat": _myRide.destLatLng.lat,
      "dest_lng": _myRide.destLatLng.lng,
      "vehicle_num": _myRide.vehicleNum
    };

    return DataService()
        .postReq(JsonEncoder().convert(data), APIPaths.UpdateRide.index);
  }

  Future<Response> _onRefreshRideLocationPressed() {
    Map<String, dynamic> data = {
      "otpHash": sha256.convert(_otpVal.codeUnits).toString(),
      "vehicle_num": ComService.myRide.value.vehicleNum
    };

    return DataService()
        .postReq(JsonEncoder().convert(data), APIPaths.GetRideLocation.index);
  }
}
