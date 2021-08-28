import 'package:flutter/material.dart';
import 'package:travel_care/Services/ComService.dart';

class RideSelection extends StatefulWidget {
  @override
  _RideSelectionState createState() => _RideSelectionState();
}

class _RideSelectionState extends State<RideSelection> {
  String? _eta, _vehicleType;
  late double _startLat, _startLong, _destLat, _destLong;

  @override
  void initState() {
    super.initState();
    _eta = 'sometime now';
    _vehicleType = 'Deluxe';

    _startLat = ComService.startLat.value;
    _startLong = ComService.startLong.value;
    _destLat = ComService.destLat.value;
    _destLong = ComService.destLong.value;

    ComService.startLat.listen((value) {
      _startLat = value;
    });
    ComService.startLong.listen((value) {
      _startLong = value;
    });
    ComService.destLat.listen((value) {
      _destLat = value;
    });
    ComService.destLong.listen((value) {
      _destLong = value;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      color: Colors.white,
      width: 250,
      child: Column(
        mainAxisAlignment: MainAxisAlignment.start,
        crossAxisAlignment: CrossAxisAlignment.center,
        children: [
          Container(
            constraints: BoxConstraints(minWidth: 250),
            color: Colors.pink,
            child: Padding(
              padding: EdgeInsets.all(20),
              child: Text(
                'Chosen Ride Details',
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
                    child:
                        Icon(Icons.location_on, color: Colors.green, size: 18),
                  ),
                  Text(
                    'Start Location',
                    style: TextStyle(color: Colors.pink, fontSize: 18),
                  ),
                ]),
          ),
          Padding(
            padding: EdgeInsets.fromLTRB(18, 0, 20, 4),
            child: Text('latitude: ' + _startLat.toString(),
                style: TextStyle(color: Colors.pink, fontSize: 12)),
          ),
          Padding(
            padding: EdgeInsets.fromLTRB(18, 0, 20, 20),
            child: Text('longitude: ' + _startLong.toString(),
                textAlign: TextAlign.right,
                style: TextStyle(color: Colors.pink, fontSize: 12)),
          ),
          Padding(
            padding: EdgeInsets.fromLTRB(14, 0, 20, 5),
            child: Flex(
                direction: Axis.horizontal,
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Padding(
                    padding: EdgeInsets.only(right: 5),
                    child:
                        Icon(Icons.location_on, color: Colors.blue, size: 18),
                  ),
                  Text(
                    'End Location',
                    style: TextStyle(color: Colors.pink, fontSize: 18),
                  ),
                ]),
          ),
          Padding(
            padding: EdgeInsets.fromLTRB(18, 0, 20, 4),
            child: Text('latitude: ' + _destLat.toString(),
                style: TextStyle(color: Colors.pink, fontSize: 12)),
          ),
          Padding(
            padding: EdgeInsets.fromLTRB(18, 0, 20, 20),
            child: Text('longitude: ' + _destLong.toString(),
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
                    child: Icon(Icons.directions_car_rounded,
                        color: Colors.purple, size: 18),
                  ),
                  DropdownButton(
                      value: _vehicleType,
                      onChanged: (String? newVal) {
                        setState(() {
                          _vehicleType = newVal;
                        });
                      },
                      style: TextStyle(color: Colors.pink),
                      items: <String>["Utility", "Deluxe", "Luxury"]
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
                      onChanged: (String? newVal) {
                        setState(() {
                          _eta = newVal;
                        });
                      },
                      style: TextStyle(color: Colors.pink),
                      items: <String>[
                        "sometime now",
                        "after 30 mins",
                        "after 1 hour"
                      ].map<DropdownMenuItem<String>>((String value) {
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
              onPressed: () {},
              child: Text('Book Ride'),
            ),
          ),
        ],
      ),
    );
  }
}
