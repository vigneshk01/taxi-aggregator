import 'dart:convert';
import 'dart:html' show DivElement;

import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:google_maps/google_maps.dart' as gmaps;
import 'dart:ui' as ui;
import 'package:my_travel_taxi/Data/checker.dart';
import 'package:my_travel_taxi/Models/PathsEnum.dart';
import 'package:my_travel_taxi/Models/StageEnum.dart';
import 'package:my_travel_taxi/Services/ComService.dart';
import 'package:my_travel_taxi/Services/DataService.dart';
import 'package:my_travel_taxi/Services/MessageService.dart';

class MapView extends StatefulWidget {
  @override
  _MapViewState createState() => _MapViewState();
}

class _MapViewState extends State<MapView> {
  late gmaps.LatLng _sourceLatLng, _destLatLng;

  late String _htmlId;

  late final gmaps.Icon _imageUtility, _imageDeluxe, _imageLuxury;

  late DivElement _elem;
  late final gmaps.GMap _map;
  late final gmaps.MapRestriction _mapRestrictions;
  late final gmaps.MapOptions _mapOptions;
  late final gmaps.Marker _sourceMarker, _destMarker, _rideMarker;
  late final gmaps.DirectionsRendererOptions direcRendOptions;
  late final gmaps.DirectionsRenderer _directionsRenderer;
  late final gmaps.DirectionsService _directionsService;
  late Map<String, gmaps.Marker> _cabMarkers;

  @override
  void initState() {
    super.initState();
    _sourceLatLng = ComService.startLatLng.value;
    _destLatLng = ComService.destLatLng.value;

    _cabMarkers = {};

    mapInit();

    ComService.startLatLng.listen((value) {
      setState(() {
        _sourceLatLng = value;
        _sourceMarker..position = value;
        directionUpdate();
      });
    });
    ComService.destLatLng.listen((value) {
      setState(() {
        _destLatLng = value;
        _destMarker..position = value;
        directionUpdate();
      });
    });
    ComService.rideLatLng.listen((value) {
      setState(() {
        _rideMarker..position = value;
      });
    });
    ComService.rideStage.listen((value) {
      Object? mapObj;
      String? title;
      gmaps.Icon? image;
      switch (value) {
        case Stage.StartRide:
        case Stage.EndRide:
          if (_cabMarkers.isNotEmpty) {
            clearMarkers();
          }
          mapObj = _map;
          title = ComService.myRide.value.vehicleNum;
          image = getTaxiMarkerImage(ComService.myRide.value.vehicleType);
          break;
        case Stage.GetARide:
        case Stage.ConfirmRide:
        case Stage.FeedbackOnRide:
          mapObj = null;
          title = null;
          break;
        default:
          mapObj = null;
          title = null;
      }
      setState(() {
        _rideMarker..map = mapObj;
        _rideMarker..title = title;
        _rideMarker..icon = image;
      });
    });

    setNearbyRidesMarkers();
    directionUpdate();
  }

  @override
  Widget build(BuildContext context) {
    return mapWidget();
  }

  void mapInit() {
    _htmlId = "RouteView";

    _imageUtility = gmaps.Icon()
      ..url = "assets/images/taxi-utility.png"
      ..scaledSize = gmaps.Size(33, 58);

    _imageDeluxe = gmaps.Icon()
      ..url = "assets/images/taxi-deluxe.png"
      ..scaledSize = gmaps.Size(33, 58);

    _imageLuxury = gmaps.Icon()
      ..url = "assets/images/taxi-luxury.png"
      ..scaledSize = gmaps.Size(33, 58);

    _mapRestrictions = gmaps.MapRestriction()
      ..latLngBounds = Checker.checkMap['mapBounds'];

    _mapOptions = gmaps.MapOptions()
      ..zoom = 15
      ..center = Checker.checkMap['mapCenter']
      ..mapTypeControl = true
      ..mapTypeControlOptions = (gmaps.MapTypeControlOptions()
        ..style = gmaps.MapTypeControlStyle.DEFAULT
        ..position = gmaps.ControlPosition.BOTTOM_RIGHT)
      ..restriction = _mapRestrictions;

    _elem = DivElement()
      ..id = _htmlId
      ..style.width = "100%"
      ..style.height = "100%"
      ..style.border = 'none';

    _map = gmaps.GMap(_elem, _mapOptions);

    _sourceMarker = gmaps.Marker(gmaps.MarkerOptions()
      ..draggable = false
      ..position = _sourceLatLng
      ..icon = (gmaps.GSymbol()
        ..path = gmaps.SymbolPath.FORWARD_CLOSED_ARROW
        ..fillColor = 'blue'
        ..fillOpacity = 1
        ..strokeColor = 'blue'
        ..strokeOpacity = 1
        ..strokeWeight = 3
        ..scale = 6)
      ..map = _map
      ..label = 'Start location');

    _destMarker = gmaps.Marker(gmaps.MarkerOptions()
      ..draggable = false
      ..position = _destLatLng
      ..icon = (gmaps.GSymbol()
        ..path = gmaps.SymbolPath.FORWARD_CLOSED_ARROW
        ..fillColor = 'violet'
        ..fillOpacity = 1
        ..strokeColor = 'violet'
        ..strokeOpacity = 1
        ..strokeWeight = 3
        ..scale = 6)
      ..map = _map
      ..label = 'Destination location');

    _rideMarker = gmaps.Marker(gmaps.MarkerOptions()
      ..draggable = false
      ..position = _destLatLng
      ..icon = null
      ..map = null);

    direcRendOptions = gmaps.DirectionsRendererOptions()..draggable = false;

    _directionsRenderer = gmaps.DirectionsRenderer()
      ..map = _map
      ..options = direcRendOptions;
    _directionsService = gmaps.DirectionsService();
  }

  Widget mapWidget() {
    // ignore: undefined_prefixed_name
    ui.platformViewRegistry.registerViewFactory(_htmlId, (int viewId) {
      return _elem;
    });

    return HtmlElementView(viewType: _htmlId);
  }

  void directionUpdate() {
    _directionsService
        .route(gmaps.DirectionsRequest()
          ..origin = _sourceLatLng
          ..destination = _destLatLng
          ..travelMode = gmaps.TravelMode.DRIVING)
        .then((response) => {_directionsRenderer..directions = response});
  }

  void setNearbyRidesMarkers() {
    Map<String, dynamic> data = {
      "lat": _sourceLatLng.lat,
      "lng": _sourceLatLng.lng
    };

    DataService()
        .postReq(JsonEncoder().convert(data), APIPaths.GetNearbyRides.index)
        .then((response) {
      if (response.statusCode == 200) {
        final List<dynamic> _cabList = json.decode(response.body);

        if (_cabMarkers.isEmpty) {
          clearMarkers();
        }
        for (dynamic cab in _cabList) {
          Map<String, dynamic> cabDets = cab;
          gmaps.Marker _cabMarker = gmaps.Marker(gmaps.MarkerOptions()
            ..draggable = false
            ..position = gmaps.LatLng(cabDets['location']['coordinates'][0],
                cabDets['location']['coordinates'][1])
            ..title = cabDets['vehicle_num']
            ..icon = getTaxiMarkerImage(cabDets['vehicle_type'])
            ..map = _map);
          setState(() {
            _cabMarkers[cabDets['vehicle_num']] = _cabMarker;
          });
        }

        MessageService.showMessage(
            context, "Nearby rides shown!", Colors.green);
      } else {
        MessageService.showMessage(
            context, "Failed to show nearby rides!", Colors.red);
        print(response.body);
      }
    }, onError: (err) {
      MessageService.showMessage(
          context, "Failed to show nearby rides!", Colors.red);
    });
  }

  gmaps.Icon getTaxiMarkerImage(vehType) {
    switch (vehType) {
      case "UTILITY":
        return _imageUtility;
      case "DELUXE":
        return _imageDeluxe;
      case "LUXURY":
        return _imageLuxury;
      default:
        return _imageUtility;
    }
  }

  void clearMarkers() {
    _cabMarkers.forEach((key, value) {
      value.map = null;
    });
    setState(() {
      _cabMarkers.clear();
    });
  }
}
