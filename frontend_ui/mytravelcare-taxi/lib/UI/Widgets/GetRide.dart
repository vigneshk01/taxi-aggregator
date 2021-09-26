import 'dart:convert';

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

class GetRide extends StatefulWidget {
  @override
  _GetRideState createState() => _GetRideState();
}

class _GetRideState extends State<GetRide> {
  late String _vehicleType, _eta;
  late String _startAddress, _destAddress;
  late gmaps.LatLng _startLatLng, _destLatLng;

  late List<String> _addressList;
  late List<gmaps.LatLng> _locList;

  late bool _onGetARidePending;

  late Ride _rideDets;

  @override
  void initState() {
    super.initState();

    _vehicleType = 'DELUXE';
    _eta = 'sometime now';

    _addressList = Checker.checkMap['endPointsAddressList'];
    _locList = Checker.checkMap['endPointsLocList'];

    _startAddress = _addressList[0];
    _destAddress = _addressList[1];

    _startLatLng = _locList[0];
    _destLatLng = _locList[1];

    _onGetARidePending = false;

    _rideDets = ComService.myRide.value;
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
                      'Get A Ride...',
                      style: TextStyle(color: Colors.white, fontSize: 22),
                    ),
                  ),
                ),
                Padding(
                  padding: EdgeInsets.fromLTRB(14, 20, 20, 5),
                  child: Flex(
                      direction: Axis.horizontal,
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Padding(
                          padding: EdgeInsets.only(right: 5),
                          child: Icon(Icons.location_on,
                              color: Colors.blue, size: 18),
                        ),
                        Text(
                          'Start Location',
                          style: TextStyle(color: Colors.pink, fontSize: 18),
                        ),
                      ]),
                ),
                Padding(
                  padding: EdgeInsets.fromLTRB(5, 10, 5, 5),
                  child: Container(
                    width: 300,
                    decoration: BoxDecoration(
                      color: Colors.white,
                      border: Border.all(color: Colors.pink),
                      borderRadius: BorderRadius.all(Radius.circular(5)),
                    ),
                    child: DropdownButton(
                        isExpanded: true,
                        value: _startAddress,
                        underline: Container(),
                        onChanged: (String? newVal) {
                          if (mounted) {
                            setState(() {
                              _startAddress = newVal!;
                              _startLatLng =
                                  _locList[_addressList.indexOf(newVal)];
                              ComService.startLatLng.add(_startLatLng);
                            });
                          }
                        },
                        items: Checker.checkMap['endPointsAddressList']
                            .map<DropdownMenuItem<String>>((String value) {
                              return DropdownMenuItem<String>(
                                value: value,
                                child: Container(
                                  alignment: Alignment.center,
                                  width: 276,
                                  child: Text(
                                    value,
                                    textAlign: TextAlign.center,
                                  ),
                                ),
                              );
                            })
                            .where((DropdownMenuItem<String> item) =>
                                item.value != _destAddress)
                            .toList()),
                  ),
                ),
                Padding(
                  padding: EdgeInsets.fromLTRB(18, 0, 20, 4),
                  child: Text(ComService.startLatLng.value.toString(),
                      style: TextStyle(color: Colors.pink, fontSize: 12)),
                ),
                Padding(
                  padding: EdgeInsets.fromLTRB(14, 20, 20, 5),
                  child: Flex(
                      direction: Axis.horizontal,
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Padding(
                          padding: EdgeInsets.only(right: 5),
                          child: Icon(Icons.location_on,
                              color: Colors.purpleAccent, size: 18),
                        ),
                        Text(
                          'End Location',
                          style: TextStyle(color: Colors.pink, fontSize: 18),
                        ),
                      ]),
                ),
                Padding(
                  padding: EdgeInsets.all(5),
                  child: Container(
                    width: 300,
                    decoration: BoxDecoration(
                      color: Colors.white,
                      border: Border.all(color: Colors.pink),
                      borderRadius: BorderRadius.all(Radius.circular(5)),
                    ),
                    child: DropdownButton(
                        isExpanded: true,
                        underline: Container(),
                        value: _destAddress,
                        onChanged: (String? newVal) {
                          if (mounted) {
                            setState(() {
                              _destAddress = newVal!;
                              _destLatLng =
                                  _locList[_addressList.indexOf(newVal)];
                              ComService.destLatLng.add(_destLatLng);
                            });
                          }
                        },
                        items: Checker.checkMap['endPointsAddressList']
                            .map<DropdownMenuItem<String>>((String value) {
                              return DropdownMenuItem<String>(
                                value: value,
                                child: Container(
                                  alignment: Alignment.center,
                                  width: 276,
                                  child: Text(
                                    value,
                                    textAlign: TextAlign.center,
                                  ),
                                ),
                              );
                            })
                            .where((DropdownMenuItem<String> item) =>
                                item.value != _startAddress)
                            .toList()),
                  ),
                ),
                Padding(
                  padding: EdgeInsets.fromLTRB(18, 0, 20, 4),
                  child: Text(ComService.destLatLng.value.toString(),
                      style: TextStyle(color: Colors.pink, fontSize: 12)),
                ),
                Padding(
                  padding: EdgeInsets.fromLTRB(18, 5, 10, 5),
                  child: Flex(
                      direction: Axis.horizontal,
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Padding(
                          padding: EdgeInsets.only(right: 5),
                          child: Icon(Icons.directions_car_rounded, size: 18),
                        ),
                        DropdownButton(
                            value: _vehicleType,
                            onChanged: (String? newval) {
                              if (mounted) {
                                setState(() {
                                  _vehicleType = newval!;
                                });
                              }
                            },
                            style: TextStyle(color: Colors.pink),
                            items: Checker.checkMap['vehicleTypeList']
                                .map<DropdownMenuItem<String>>((String value) {
                              return DropdownMenuItem<String>(
                                value: value,
                                child: Text(value),
                              );
                            }).toList()),
                      ]),
                ),
                Padding(
                  padding: EdgeInsets.fromLTRB(18, 5, 10, 5),
                  child: Flex(
                      direction: Axis.horizontal,
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Padding(
                          padding: EdgeInsets.only(right: 5),
                          child: Icon(Icons.timer, size: 18),
                        ),
                        DropdownButton(
                            value: _eta,
                            onChanged: (String? newval) {
                              if (mounted) {
                                setState(() {
                                  _eta = newval!;
                                });
                              }
                            },
                            style: TextStyle(color: Colors.pink),
                            items: Checker.checkMap['scheduleTimeList']
                                .map<DropdownMenuItem<String>>((String value) {
                              return DropdownMenuItem<String>(
                                value: value,
                                child: Text(value),
                              );
                            }).toList()),
                      ]),
                ),
                Padding(
                  padding: EdgeInsets.all(20),
                  child: ElevatedButton(
                    onPressed: () {
                      if (mounted) {
                        setState(() {
                          _onGetARidePending = true;
                        });
                      }
                      _onGetRidePressed().then((response) {
                        if (mounted) {
                          setState(() {
                            _onGetARidePending = false;
                          });
                        }
                        if (response.statusCode == 200) {
                          final body = json.decode(response.body);
                          setRide(body);
                          MessageService.showMessage(
                              context, "Get A Ride Successful!", Colors.green);
                        } else {
                          MessageService.showMessage(
                              context, "Get A Ride Failed!", Colors.red);
                        }
                      }, onError: (_) {
                        if (mounted) {
                          setState(() {
                            _onGetARidePending = false;
                          });
                        }
                        MessageService.showMessage(
                            context, "Get A Ride Failed!", Colors.red);
                      });
                    },
                    child: Text('Get A Ride'),
                  ),
                ),
                Padding(
                  padding: EdgeInsets.all(20),
                  child: ElevatedButton(
                    onPressed: () {
                      if (mounted) {
                        setState(() {
                          _onGetARidePending = true;
                        });
                      }
                      _onShowRidesPressed("NearbyRides").then((response) {
                        if (mounted) {
                          setState(() {
                            _onGetARidePending = false;
                          });
                        }
                        if (response.statusCode == 200) {
                          final List<dynamic> _cabList =
                              json.decode(response.body);
                          ComService.nearbyRides.add(_cabList);

                          MessageService.showMessage(
                              context, "Nearby rides shown!", Colors.green);
                        } else {
                          MessageService.showMessage(context,
                              "Failed to show nearby rides!", Colors.red);
                          print(response.body);
                        }
                      }, onError: (err) {
                        if (mounted) {
                          setState(() {
                            _onGetARidePending = false;
                          });
                        }
                        MessageService.showMessage(context,
                            "Failed to show nearby rides!", Colors.red);
                      });
                    },
                    child: Text('Nearby Rides'),
                  ),
                ),
                Padding(
                  padding: EdgeInsets.all(20),
                  child: ElevatedButton(
                    onPressed: () {
                      if (mounted) {
                        setState(() {
                          _onGetARidePending = true;
                        });
                      }
                      _onShowRidesPressed("AllTaxis").then((response) {
                        if (mounted) {
                          setState(() {
                            _onGetARidePending = false;
                          });
                        }
                        if (response.statusCode == 200) {
                          final List<dynamic> _cabList =
                              json.decode(response.body);
                          ComService.nearbyRides.add(_cabList);

                          MessageService.showMessage(
                              context, "All taxis shown!", Colors.green);
                        } else {
                          MessageService.showMessage(
                              context, "Failed to show all taxis!", Colors.red);
                          print(response.body);
                        }
                      }, onError: (err) {
                        if (mounted) {
                          setState(() {
                            _onGetARidePending = false;
                          });
                        }
                        MessageService.showMessage(
                            context, "Failed to show all taxis!", Colors.red);
                      });
                    },
                    child: Text('All Taxis'),
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
      Visibility(
        visible: _onGetARidePending,
        child: Container(
          width: 300,
          child: LinearProgressIndicator(
            color: Colors.yellow,
          ),
        ),
      ),
    ]);
  }

  Future<Response> _onGetRidePressed() {
    Map<String, dynamic> data = {
      "start_lat": ComService.startLatLng.value.lat,
      "start_lng": ComService.startLatLng.value.lng,
      "dest_lat": ComService.destLatLng.value.lat,
      "dest_lng": ComService.destLatLng.value.lng,
      "vehicle_type": _vehicleType
    };

    return DataService()
        .postReq(JsonEncoder().convert(data), APIPaths.GetARide.index);
  }

  Future<Response> _onShowRidesPressed(String type) {
    Map<String, dynamic> data = {
      "lat": ComService.startLatLng.value.lat,
      "lng": ComService.startLatLng.value.lng
    };

    if (type == "NearbyRides") {
      return DataService()
          .postReq(JsonEncoder().convert(data), APIPaths.GetNearbyRides.index);
    } else if (type == "AllTaxis") {
      return DataService().getReq(APIPaths.AllTaxis.index);
    } else {
      return Future.error("invalid type");
    }
  }

  setRide(body) {
    _rideDets.init();

    _rideDets.startAddress = _startAddress;
    _rideDets.destAddress = _destAddress;

    _rideDets.startLatLng = _startLatLng;
    _rideDets.destLatLng = _destLatLng;

    _rideDets.scheduledTime = DateTime.now().toIso8601String();
    _rideDets.vehicleType = _vehicleType;

    switch (_eta) {
      case "sometime now":
        _rideDets.scheduledTime = DateTime.now().toIso8601String();
        break;
      case "after 30 mins":
        //_rideDets.scheduledTime = DateTime.now().add(Duration(minutes: 30));
        _rideDets.scheduledTime = DateTime.now().toIso8601String();
        break;
      case "after 1 hour":
        //_rideDets.scheduledTime = DateTime.now().add(Duration(hours: 1));
        _rideDets.scheduledTime = DateTime.now().toIso8601String();
        break;
      default:
        _rideDets.scheduledTime = DateTime.now().toIso8601String();
        break;
    }

    _rideDets.setFromJSON(body);

    ComService.myRide.add(_rideDets);
    ComService.rideStage.add(Stage.ConfirmRide);
  }
}
