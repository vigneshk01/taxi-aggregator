import 'dart:convert';

import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:google_maps/google_maps.dart' as gmaps;
import 'package:http/http.dart';
import 'package:my_travel_taxi/Models/PathsEnum.dart';
import 'package:my_travel_taxi/Models/Ride.dart';
import 'package:my_travel_taxi/Models/StageEnum.dart';
import 'package:my_travel_taxi/Models/TaxiUser.dart';
import 'package:my_travel_taxi/Services/ComService.dart';
import 'package:my_travel_taxi/Services/DataService.dart';
import 'package:my_travel_taxi/Services/MessageService.dart';

import 'BookedState.dart';

class ThisTaxi extends StatefulWidget {
  @override
  _ThisTaxiState createState() => _ThisTaxiState();
}

class _ThisTaxiState extends State<ThisTaxi> {
  late bool _onThisTaxiPending;
  late double _startLat, _startLng, _destLat, _destLng;

  @override
  void initState() {
    super.initState();
    _onThisTaxiPending = false;
    _startLat = 0;
    _startLng = 0;
    _destLat = 0;
    _destLng = 0;
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
                      'This Taxi...',
                      style: TextStyle(color: Colors.white, fontSize: 22),
                    ),
                  ),
                ),
                Padding(
                  padding: EdgeInsets.all(20),
                  child: ElevatedButton(
                    onPressed: () {
                      if (mounted) {
                        setState(() {
                          _onThisTaxiPending = true;
                        });
                      }
                      _onRefreshTaxiStatePressed().then((response) {
                        if (mounted) {
                          setState(() {
                            _onThisTaxiPending = false;
                          });
                        }
                        if (response.statusCode == 200) {
                          final Map<String, dynamic> _rideLoc =
                              json.decode(response.body);
                          final List<dynamic> _currentRide =
                              _rideLoc['current_ride'];
                          TaxiUser _taxiUser = ComService.taxiUser.value;
                          if (_currentRide.isNotEmpty) {
                            ComService.isBooked.add(true);
                            _taxiUser.status = "BOOKED";
                            if (_startLat !=
                                    _currentRide[0]['start_loc']['coordinates']
                                        [0] &&
                                _startLng !=
                                    _currentRide[0]['start_loc']['coordinates']
                                        [1]) {
                              _startLat = _currentRide[0]['start_loc']['coordinates']
                              [0];
                              _startLng = _currentRide[0]['start_loc']['coordinates']
                              [1];
                              ComService.startLatLng.add(gmaps.LatLng(
                                  _currentRide[0]['start_loc']['coordinates']
                                      [0],
                                  _currentRide[0]['start_loc']['coordinates']
                                      [1]));
                            }
                            if (_destLat !=
                                    _currentRide[0]['dest_loc']['coordinates']
                                        [0] &&
                                _destLng !=
                                    _currentRide[0]['dest_loc']['coordinates']
                                        [1]) {
                              _destLat = _currentRide[0]['dest_loc']['coordinates']
                              [0];
                              _destLng = _currentRide[0]['dest_loc']['coordinates']
                              [1];
                              ComService.destLatLng.add(gmaps.LatLng(
                                  _currentRide[0]['dest_loc']['coordinates'][0],
                                  _currentRide[0]['dest_loc']['coordinates']
                                      [1]));
                            }
                            ComService.rideLatLng.add(gmaps.LatLng(
                                _currentRide[0]['current_vehicle_location']
                                    ['coordinates'][0],
                                _currentRide[0]['current_vehicle_location']
                                    ['coordinates'][1]));
                            Ride _rideDets = ComService.myRide.value;
                            _rideDets.init();
                            _rideDets.startAddress =
                                _currentRide[0]['start_address'];
                            _rideDets.destAddress =
                                _currentRide[0]['dest_address'];
                            _rideDets.bookedTime =
                                _currentRide[0]['booked_time'];
                            _rideDets.startTime = _currentRide[0]['start_time'];
                            _rideDets.endTime = _currentRide[0]['end_time'];
                            _rideDets.status = _currentRide[0]['status'];
                            ComService.myRide.add(_rideDets);
                          } else {
                            _taxiUser.status = _rideLoc["status"];
                            ComService.isBooked.add(false);
                            ComService.rideStage.add(Stage.ThisTaxi);
                            ComService.startLatLng.add(gmaps.LatLng(0, 0));
                            ComService.destLatLng.add(gmaps.LatLng(0, 0));
                            ComService.rideLatLng.add(gmaps.LatLng(
                                _rideLoc['location']['coordinates'][0],
                                _rideLoc['location']['coordinates'][1]));
                          }
                          ComService.taxiUser.add(_taxiUser);
                          MessageService.showMessage(
                              context, "Taxi state updated!", Colors.green);
                        } else {
                          MessageService.showMessage(context,
                              "Failed to update taxi state!", Colors.red);
                        }
                      }, onError: (err) {
                        if (mounted) {
                          setState(() {
                            _onThisTaxiPending = false;
                          });
                        }
                        MessageService.showMessage(context,
                            "Failed to update taxi state!", Colors.red);
                      });
                    },
                    child: Text('Refresh Taxi State'),
                  ),
                ),
                ComService.isBooked.value
                    ? BookedState()
                    : Text(
                        "Not Booked right now!",
                        style: TextStyle(color: Colors.pink),
                      )
              ],
            ),
          ),
        ),
      ),
      Visibility(
        visible: _onThisTaxiPending,
        child: Container(
          width: 300,
          child: LinearProgressIndicator(
            color: Colors.yellow,
          ),
        ),
      )
    ]);
  }

  Future<Response> _onRefreshTaxiStatePressed() {
    Map<String, dynamic> data = {
      "vehicle_num": ComService.taxiUser.value.vehicleNum
    };

    return DataService().postReq(
        JsonEncoder().convert(data), APIPaths.GetCurrentTaxiData.index);
  }
}
