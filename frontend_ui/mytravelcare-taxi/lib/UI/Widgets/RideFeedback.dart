import 'dart:convert';

import 'package:crypto/crypto.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:http/http.dart';
import 'package:my_travel_taxi/Models/PathsEnum.dart';
import 'package:my_travel_taxi/Models/Ride.dart';
import 'package:my_travel_taxi/Models/StageEnum.dart';
import 'package:my_travel_taxi/Services/ComService.dart';
import 'package:my_travel_taxi/Services/DataService.dart';
import 'package:my_travel_taxi/Services/MessageService.dart';

class RideFeedback extends StatefulWidget {
  @override
  _RideFeedbackState createState() => _RideFeedbackState();
}

class _RideFeedbackState extends State<RideFeedback> {
  late Ride _myRide;
  late bool _onRideFeedbackPending;
  late String _comments;
  late double _rating;
  late String _otpVal;

  @override
  void initState() {
    super.initState();
    _myRide = ComService.myRide.value;
    _onRideFeedbackPending = false;
    _comments = '';
    _rating = 0.0;
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
                      'Feedback...',
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
                    'Start Time:',
                    style: TextStyle(color: Colors.pink, fontSize: 14),
                  ),
                ),
                Padding(
                  padding: EdgeInsets.fromLTRB(14, 0, 20, 5),
                  child: Text(
                    _myRide.startTime,
                    style: TextStyle(fontSize: 14),
                  ),
                ),
                Padding(
                  padding: EdgeInsets.fromLTRB(14, 20, 20, 5),
                  child: Text(
                    'End Time:',
                    style: TextStyle(color: Colors.pink, fontSize: 14),
                  ),
                ),
                Padding(
                  padding: EdgeInsets.fromLTRB(14, 0, 20, 5),
                  child: Text(
                    _myRide.endTime,
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
                  padding: EdgeInsets.fromLTRB(14, 20, 20, 5),
                  child: Text(
                    'Rate the ride:',
                    style: TextStyle(color: Colors.pink, fontSize: 14),
                  ),
                ),
                Padding(
                  padding: EdgeInsets.fromLTRB(14, 5, 20, 5),
                  child: Slider(
                    min: 0,
                    max: 5,
                    label: _rating.toString(),
                    divisions: 5,
                    value: _rating,
                    onChanged: (value) {
                      if (mounted) {
                        setState(() {
                          _rating = value;
                        });
                      }
                    },
                  ),
                ),
                Padding(
                  padding: EdgeInsets.all(20),
                  child: Container(
                    width: 300,
                    child: TextFormField(
                      maxLines: 4,
                      maxLength: 100,
                      textAlign: TextAlign.center,
                      decoration: InputDecoration(
                        hintText: "Comments",
                        filled: true,
                        fillColor: Colors.white,
                      ),
                      validator: (value) {
                        if (value == null || value.isEmpty) {
                          return 'Please enter comments';
                        }
                        return null;
                      },
                      onChanged: (value) {
                        if (mounted) {
                          setState(() {
                            _comments = value;
                          });
                        }
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
                          _onRideFeedbackPending = true;
                        });
                      }
                      _onRideFeedbackPressed().then((response) {
                        if (mounted) {
                          setState(() {
                            _onRideFeedbackPending = false;
                          });
                        }
                        if (response.statusCode == 200) {
                          final Map<String, dynamic> body =
                              json.decode(response.body);
                          _myRide.passengerRating = body['passenger_rating'];
                          _myRide.passengerComments =
                              body['passenger_comments'];
                          ComService.myRide.add(_myRide);
                          ComService.rideStage.add(Stage.GetARide);
                          MessageService.showMessage(
                              context, "Thank you!", Colors.green);
                        } else {
                          MessageService.showMessage(
                              context, "Feedback failed!", Colors.red);
                        }
                      }, onError: (_) {
                        if (mounted) {
                          setState(() {
                            _onRideFeedbackPending = false;
                          });
                        }
                        MessageService.showMessage(
                            context, "Feedback failed!", Colors.red);
                      });
                    },
                    child: Text('Submit'),
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
      Visibility(
        visible: _onRideFeedbackPending,
        child: Container(
          width: 300,
          child: LinearProgressIndicator(
            color: Colors.yellow,
          ),
        ),
      )
    ]);
  }

  Future<Response> _onRideFeedbackPressed() {
    Map<String, dynamic> data = {
      "update_type": "feedback",
      "apiKey": ComService.apiKey.value,
      "OTPHash": sha256.convert(_otpVal.codeUnits).toString(),
      "passenger_rating": _rating.toString(),
      "passenger_comments": _comments,
    };

    return DataService()
        .postReq(JsonEncoder().convert(data), APIPaths.UpdateRide.index);
  }
}
