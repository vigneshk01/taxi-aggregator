import 'dart:async';
import 'dart:html';

import 'package:flutter/material.dart';
import 'package:flutter_polyline_points/flutter_polyline_points.dart';
import 'package:google_maps_flutter/google_maps_flutter.dart';
import 'package:travel_care/Data/Nearby-Cabs-Loc.dart';
import 'package:travel_care/Data/checker.dart';
import 'package:travel_care/Services/ComService.dart';

class MapView extends StatefulWidget {
  @override
  _MapViewState createState() => _MapViewState();
}

class _MapViewState extends State<MapView> {
  late double _startLat, _startLong;
  late double _destLat, _destLong;

  late Completer<GoogleMapController> _controller;

  late final LatLng _center;

  late Marker startMarker, destMarker;
  late Set<Marker> _markers;

  late PolylinePoints polyLinePoints;
  List<LatLng> polyLineCoordinates = [];
  Map<PolylineId, Polyline> polyLines = {};
  late PolylineId id = PolylineId('mytravelroute');
  late BitmapDescriptor bitmapDescriptor;
  late Polyline polyLine;

  @override
  void initState() {
    super.initState();

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

    _center = LatLng(_startLat, _startLong);

    _controller = Completer();

    startMarker = Marker(
        markerId: MarkerId('startMarker'),
        icon: BitmapDescriptor.defaultMarkerWithHue(BitmapDescriptor.hueGreen),
        draggable: true,
        position: LatLng(_startLat, _startLong),
        infoWindow: InfoWindow(
            title: 'Start location',
            snippet: 'Taxi will pick you up from near here'),
        onDragEnd: (newLoc) {
          setState(() {
            ComService.setStartLat(newLoc.latitude);
            ComService.setStartLong(newLoc.longitude);
          });
        });

    destMarker = Marker(
        markerId: MarkerId('destMarker'),
        icon: BitmapDescriptor.defaultMarkerWithHue(BitmapDescriptor.hueBlue),
        draggable: true,
        position: LatLng(_destLat, _destLong),
        infoWindow: InfoWindow(
            title: 'Destination location',
            snippet: 'Taxi will drop you near here'),
        onDragEnd: (newLoc) {
          setState(() {
            ComService.setDestLat(newLoc.latitude);
            ComService.setDestLong(newLoc.longitude);
          });
        });

    _markers = Set<Marker>();
    _markers.add(startMarker);
    _markers.add(destMarker);

  }

  void _onMapCreated(GoogleMapController controller) {
    _controller.complete(controller);
    _nearbyCabsMarker();
    _createPolyLines();
    setState(() {});
  }

  @override
  Widget build(BuildContext context) {
    return GoogleMap(
      onMapCreated: _onMapCreated,
      initialCameraPosition: CameraPosition(
        target: _center,
        zoom: 17.0,
      ),
      markers: _markers,
      polylines: Set<Polyline>.of(polyLines.values),
    );
  }

  _nearbyCabsMarker() {
    NearbyCabsLoc.nearbyCabs.asMap().forEach((index, loc) async {
      print(loc.toString() + 'nearby_taxi_' + index.toString());
      Marker nearbyCabs = Marker(
        markerId: MarkerId(loc.toString() + 'nearby_taxi_' + index.toString()),
        icon: await BitmapDescriptor.fromAssetImage(
            ImageConfiguration(), 'images/cab-icon.png'),
        position: LatLng(loc[0], loc[1]),
        draggable: false,
      );
      _markers.add(nearbyCabs);
    });
  }

  // Create the polyLines for showing the route between two places

  _createPolyLines() async {
    // Initializing polyLinePoints
    polyLinePoints = PolylinePoints();

    // Generating the list of coordinates to be used for
    // drawing the polyLines
    PolylineResult result = await polyLinePoints.getRouteBetweenCoordinates(
      (Checker.checkMap['maps-key'])!, // Google Maps API Key
      PointLatLng(_startLat, _startLong),
      PointLatLng(_destLat, _destLong),
      travelMode: TravelMode.transit,
    );

    polyLineCoordinates.clear();

    // Adding the coordinates to the list
    if (result.points.isNotEmpty) {
      result.points.forEach((PointLatLng point) {
        polyLineCoordinates.add(LatLng(point.latitude, point.longitude));
      });
    }

    polyLine = Polyline(
      polylineId: id,
      color: Colors.red,
      points: polyLineCoordinates,
      width: 3,
    );

    polyLines[id] = polyLine;

    setState(() {});
  }
}
