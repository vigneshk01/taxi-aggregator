import 'dart:convert';

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
                      'Confirm...',
                      style: TextStyle(color: Colors.white, fontSize: 22),
                    ),
                  ),
                ),
                Padding(
                  padding: EdgeInsets.fromLTRB(14, 20, 20, 5),
                  child: Text(
                    'From:',
                    style: TextStyle(color: Colors.pink, fontSize: 14),
                  ),
                ),
                Padding(
                  padding: EdgeInsets.fromLTRB(14, 0, 20, 5),
                  child: Text(
                    _myRide.startAddress,
                    textAlign: TextAlign.center,
                    style: TextStyle(fontSize: 14),
                  ),
                ),
                Padding(
                  padding: EdgeInsets.fromLTRB(14, 20, 20, 5),
                  child: Text(
                    'To:',
                    style: TextStyle(color: Colors.pink, fontSize: 14),
                  ),
                ),
                Padding(
                  padding: EdgeInsets.fromLTRB(14, 0, 20, 5),
                  child: Text(
                    _myRide.destAddress,
                    textAlign: TextAlign.center,
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
                    'Scheduled Time:',
                    style: TextStyle(color: Colors.pink, fontSize: 14),
                  ),
                ),
                Padding(
                  padding: EdgeInsets.fromLTRB(14, 0, 20, 5),
                  child: Text(
                    _myRide.scheduledTime.toString(),
                    style: TextStyle(fontSize: 14),
                  ),
                ),
                Padding(
                  padding: EdgeInsets.fromLTRB(14, 20, 20, 5),
                  child: Text(
                    'Cost:',
                    style: TextStyle(color: Colors.pink, fontSize: 14),
                  ),
                ),
                Padding(
                  padding: EdgeInsets.fromLTRB(14, 0, 20, 5),
                  child: Text(
                    _myRide.cost,
                    style: TextStyle(fontSize: 14),
                  ),
                ),
                Padding(
                  padding: EdgeInsets.all(20),
                  child: ElevatedButton(
                    onPressed: () {
                      if (mounted) {
                        setState(() {
                          _onCofirmRidePending = true;
                        });
                      }
                      _onConfirmRidePressed().then((response) {
                        if (mounted) {
                          setState(() {
                            _onCofirmRidePending = false;
                          });
                        }
                        if (response.statusCode == 200) {
                          final Map<String, dynamic> body =
                              json.decode(response.body);
                          ComService.otp.add(body['OTP'].toString());
                          ComService.rideStage.add(Stage.StartRide);
                          MessageService.showMessage(context,
                              "Confirm Ride Successful!", Colors.green);
                        } else {
                          MessageService.showMessage(
                              context, "Confirm Ride Failed!", Colors.red);
                        }
                      }, onError: (_) {
                        if (mounted) {
                          setState(() {
                            _onCofirmRidePending = true;
                          });
                        }
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
      ),
      Visibility(
        visible: _onCofirmRidePending,
        child: Container(
          width: 300,
          child: LinearProgressIndicator(
            color: Colors.yellow,
          ),
        ),
      )
    ]);
  }

  Future<Response> _onConfirmRidePressed() {
    Map<String, dynamic> data = {
      "apiKey": ComService.apiKey.value,
      "start_address": _myRide.startAddress,
      "dest_address": _myRide.destAddress,
      "start_lat": _myRide.startLatLng.lat,
      "start_lng": _myRide.startLatLng.lng,
      "dest_lat": _myRide.destLatLng.lat,
      "dest_lng": _myRide.destLatLng.lng,
      "booked_time": DateTime.now().toIso8601String(),
      "scheduled_time": _myRide.scheduledTime,
      "vehicle_num": _myRide.vehicleNum,
      "vehicle_type": _myRide.vehicleType
    };

    return DataService()
        .postReq(JsonEncoder().convert(data), APIPaths.ConfirmRide.index);
  }
}
