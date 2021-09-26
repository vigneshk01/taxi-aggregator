import 'dart:async';
import 'dart:html' show DivElement;
import 'dart:math';

import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:google_maps/google_maps.dart' as gmaps;
import 'dart:ui' as ui;
import 'package:my_travel_taxi/Data/checker.dart';
import 'package:my_travel_taxi/Models/StageEnum.dart';
import 'package:my_travel_taxi/Services/ComService.dart';

class MapView extends StatefulWidget {
  @override
  _MapViewState createState() => _MapViewState();
}

class _MapViewState extends State<MapView> {
  late gmaps.LatLng _sourceLatLng, _destLatLng;

  late String _htmlId;

  late final gmaps.Icon _imageUtility,
      _imageDeluxe,
      _imageLuxury,
      _imageBooked,
      _imageInactive;

  late DivElement _elem;
  late final gmaps.GMap _map;
  late final gmaps.MapRestriction _mapRestrictions;
  late final gmaps.MapOptions _mapOptions;
  late final gmaps.Marker _sourceMarker, _destMarker, _rideMarker;
  late final gmaps.DirectionsRendererOptions direcRendOptions;
  late final gmaps.DirectionsRenderer _directionsRenderer;
  late final gmaps.DirectionsService _directionsService;
  late Map<String, gmaps.Marker> _cabMarkers;
  late List<StreamSubscription> subsList;

  @override
  void initState() {
    super.initState();

    _sourceLatLng = ComService.startLatLng.value;
    _destLatLng = ComService.destLatLng.value;

    _cabMarkers = Map();

    mapInit();

    subsList = [];

    subsList.add(ComService.startLatLng.listen((value) {
      if (mounted) {
        setState(() {
          _sourceLatLng = value;
          _sourceMarker..position = value;
          if(ComService.rideStage.value.index != Stage.ThisTaxi.index) {
            directionUpdate();
          }
        });
      }
    }));

    subsList.add(ComService.destLatLng.listen((value) {
      if (mounted) {
        setState(() {
          _destLatLng = value;
          _destMarker..position = value;
          if(ComService.rideStage.value.index != Stage.ThisTaxi.index) {
            directionUpdate();
          }
        });
      }
    }));

    subsList.add(ComService.rideLatLng.listen((value) {
      if (mounted) {
        setState(() {
          _rideMarker..position = value;
        });
      }
    }));

    subsList.add(ComService.nearbyRides.listen((value) {
      if (_cabMarkers.isNotEmpty || value.isEmpty) {
        clearMarkers();
      }
      for (dynamic cab in value) {
        Map<String, dynamic> cabDets = cab;
        String vehStatus = cabDets['status'] ?? "ACTIVE";
        gmaps.Marker _cabMarker = gmaps.Marker(gmaps.MarkerOptions()
          ..draggable = false
          ..position = gmaps.LatLng(cabDets['location']['coordinates'][0],
              cabDets['location']['coordinates'][1])
          ..title = cabDets['vehicle_num'] +
              '  ' +
              cabDets['vehicle_type'] +
              ' ' +
              vehStatus
          ..icon = getTaxiMarkerImage(vehStatus, cabDets['vehicle_type'])
          ..map = _map);
        if (mounted) {
          setState(() {
            _cabMarkers[cabDets['vehicle_num']] = _cabMarker;
          });
        }
      }
    }));

    subsList.add(ComService.rideStage.listen((value) {
      switch (value) {
        case Stage.StartRide:
        case Stage.EndRide:
          if (_cabMarkers.isNotEmpty) {
            clearMarkers();
          }
          if (mounted) {
            setState(() {
              _rideMarker..map = _map;
              _rideMarker..title = ComService.myRide.value.vehicleNum;
              _rideMarker..icon = getTaxiMarkerImage("ACTIVE",
                  ComService.myRide.value.vehicleType);
            });
          }
          break;
        case Stage.GetARide:
        case Stage.ConfirmRide:
        case Stage.FeedbackOnRide:
          if (mounted) {
            setState(() {
              _rideMarker..map = null;
              _rideMarker..title = null;
              _rideMarker..icon = null;
            });
          }
          break;
        case Stage.ThisTaxi:
          if (mounted) {
            setState(() {
              _rideMarker..map = _map;
              _rideMarker..title = ComService.taxiUser.value.vehicleNum;
              _rideMarker..icon = getTaxiMarkerImage(ComService.taxiUser.value.status,
                  ComService.taxiUser.value.vehicleType);
              if(ComService.isBooked.value == false) {
               _sourceMarker..map = null;
               _destMarker..map = null;
              } else {
                _sourceMarker..map = _map;
                _destMarker..map = _map;
              }
            });
          }
          break;
        default:
          if (mounted) {
            setState(() {
              _rideMarker..map = null;
              _rideMarker..title = null;
              _rideMarker..icon = null;
            });
          }
          break;
      }

    }));

    if(ComService.rideStage.value.index != Stage.ThisTaxi.index) {
      directionUpdate();
    }
  }

  @override
  void dispose() {
    super.dispose();
    subsList.map((e) => e.cancel());
    subsList.clear();
    _cabMarkers.forEach((key, value) {
      value.map = null;
    });
    _cabMarkers.clear();
    _sourceMarker..map = null;
    _destMarker..map = null;
    _rideMarker..map = null;
  }

  @override
  Widget build(BuildContext context) {
    return mapWidget();
  }

  void mapInit() {
    _htmlId = Random().nextDouble().toStringAsExponential();

    _imageUtility = gmaps.Icon()
      ..url = "assets/images/taxi-utility.png"
      ..scaledSize = gmaps.Size(33, 58);

    _imageDeluxe = gmaps.Icon()
      ..url = "assets/images/taxi-deluxe.png"
      ..scaledSize = gmaps.Size(33, 58);

    _imageLuxury = gmaps.Icon()
      ..url = "assets/images/taxi-luxury.png"
      ..scaledSize = gmaps.Size(33, 58);

    _imageInactive = gmaps.Icon()
      ..url = "assets/images/taxi-inactive.png"
      ..scaledSize = gmaps.Size(33, 58);

    _imageBooked = gmaps.Icon()
      ..url = "assets/images/taxi-booked.png"
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

  gmaps.Icon getTaxiMarkerImage(status, vehType) {
    if (status == "BOOKED") {
      return _imageBooked;
    } else if (status == "INACTIVE") {
      return _imageInactive;
    } else if (status == "ACTIVE") {
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
    } else {
      return _imageInactive;
    }
  }

  void clearMarkers() {
    _cabMarkers.forEach((key, value) {
      value.map = null;
    });
    if (mounted) {
      setState(() {
        _cabMarkers.clear();
      });
    }
  }
}
