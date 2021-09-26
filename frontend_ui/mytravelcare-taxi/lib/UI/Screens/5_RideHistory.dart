import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:http/http.dart';
import 'package:my_travel_taxi/Models/PathsEnum.dart';
import 'package:my_travel_taxi/Services/ComService.dart';
import 'package:my_travel_taxi/Services/DataService.dart';
import 'package:my_travel_taxi/Services/MessageService.dart';
import 'package:my_travel_taxi/UI/Widgets/RideItem.dart';

class RideHistory extends StatefulWidget {
  @override
  _RideHistoryState createState() => _RideHistoryState();
}

class _RideHistoryState extends State<RideHistory> {
  late List<Map<String, dynamic>> _rideHist;
  late bool _onGetHistoryPending;
  late String _userType;

  @override
  void initState() {
    // TODO: implement initState
    super.initState();

    _onGetHistoryPending = false;
    _rideHist = ComService.rideHistory.value;
    _userType = ComService.userType.value;

    ComService.rideHistory.listen((value) {
      _rideHist = value;
    });
    print(ComService.taxiUser.value);
  }

  @override
  Widget build(BuildContext context) {
    return WillPopScope(
      onWillPop: () async => true,
      child: Scaffold(
        appBar: AppBar(
          title: Text("Ride Booking History"),
          centerTitle: true,
        ),
        body: Stack(children: [
          SingleChildScrollView(
            child: Column(
              children: [
                Padding(
                  padding: EdgeInsets.all(20),
                  child: ElevatedButton(
                    onPressed: () {
                      if (mounted) {
                        setState(() {
                          _onGetHistoryPending = true;
                        });
                      }
                      _getHistory().then((response) {
                        if (mounted) {
                          setState(() {
                            _onGetHistoryPending = false;
                          });
                        }
                        if (response.statusCode == 200) {
                          MessageService.showMessage(
                              context, "ride history displayed!", Colors.green);
                          final List<dynamic> body = json.decode(response.body);
                          List<Map<String, dynamic>> _rh = [];
                          body.forEach((element) {
                            Map<String, dynamic> _rideDet = element;
                            _rh.add(_rideDet);
                          });
                          ComService.rideHistory.add(_rh);
                        }
                      }, onError: (_) {
                        MessageService.showMessage(
                            context, "Failed to get history!", Colors.red);
                      });
                    },
                    child: Text('Refresh'),
                  ),
                ),
                Padding(
                  padding: EdgeInsets.all(20),
                  child: Center(
                    child: ListView.builder(
                        shrinkWrap: true,
                        itemCount: _rideHist.length,
                        itemBuilder: (BuildContext context, int index) {
                          return RideItem(
                              from: _rideHist[index]['start_address'],
                              to: _rideHist[index]['dest_address'],
                              startLoc: '[' +
                                  _rideHist[index]['start_loc']['coordinates']
                                          [0]
                                      .toString() +
                                  ', ' +
                                  _rideHist[index]['start_loc']['coordinates']
                                          [1]
                                      .toString() +
                                  ']',
                              endLoc: '[' +
                                  _rideHist[index]['dest_loc']['coordinates'][0]
                                      .toString() +
                                  ', ' +
                                  _rideHist[index]['dest_loc']['coordinates'][1]
                                      .toString() +
                                  ']',
                              bookedTime: _rideHist[index]['booked_time'],
                              startTime: _rideHist[index]['start_time'],
                              endTime: _rideHist[index]['end_time'],
                              vehicleType: _rideHist[index]['vehicle_type'],
                              vehicleNum: _rideHist[index]['vehicle_num'],
                              cost: _rideHist[index]['cost'],
                              passengerRating: _rideHist[index]
                                  ['passenger_rating'],
                              passengerComments: _rideHist[index]
                                  ['passenger_comments'],
                              estTime: _rideHist[index]['est_time'],
                              totalDist: _rideHist[index]['total_distance'],
                              status: _rideHist[index]['status']);
                        }),
                  ),
                ),
              ],
            ),
          ),
          Visibility(
            visible: _onGetHistoryPending,
            child: LinearProgressIndicator(),
          )
        ]),
      ),
    );
  }

  Future<Response> _getHistory() {
    Map<String, String> data = {};

    if (_userType == "Taxi") {
      data = {
        "vehicle_num": ComService.taxiUser.value.vehicleNum,
        "user_type": _userType
      };
    } else if (_userType == "Passenger") {
      data = {"apiKey": ComService.apiKey.value, "user_type": _userType};
    }

    return DataService()
        .postReq(JsonEncoder().convert(data), APIPaths.GetRideHistory.index);
  }
}
