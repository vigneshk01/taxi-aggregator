import 'dart:html';

import 'package:flutter/cupertino.dart';
import 'package:google_maps/google_maps.dart' as gmaps;
import 'package:google_maps/google_maps.dart';
import 'dart:ui' as ui;
import 'package:my_travel_taxi/Data/Nearby-Cabs-Loc.dart';
import 'package:my_travel_taxi/Data/checker.dart';
import 'package:my_travel_taxi/Services/ComService.dart';

class MapView extends StatefulWidget {
  @override
  _MapViewState createState() => _MapViewState();
}

class _MapViewState extends State<MapView> {

  late LatLng _sourceLatLng,_destLatLng;

  late String _htmlId;

  late DivElement _elem;
  late gmaps.Marker _sourceMarker, _destMarker;
  late gmaps.DirectionsRenderer _directionsRenderer;
  late gmaps.DirectionsService _directionsService;

  @override
  void initState() {
    super.initState();
    _sourceLatLng = ComService.startLatLng.value;
    _destLatLng = ComService.destLatLng.value;

    _htmlId = "RouteView";

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

    directionUpdate();
  }

  @override
  Widget build(BuildContext context) {
    return mapWidget();
  }

  Widget mapWidget() {

    // ignore: undefined_prefixed_name
    ui.platformViewRegistry.registerViewFactory(_htmlId, (int viewId) {
      return _elem;
    });

    return HtmlElementView(viewType: _htmlId);
  }

  mapInit() {
    gmaps.MapRestriction _mapRestrictions = gmaps.MapRestriction()
      ..latLngBounds = Checker.checkMap['mapBounds'];

    gmaps.MapOptions _mapOptions = gmaps.MapOptions()
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

    gmaps.GMap _map = gmaps.GMap(_elem, _mapOptions);

    _sourceMarker = gmaps.Marker(gmaps.MarkerOptions()
      ..draggable = true
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
      ..draggable = true
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

    final gmaps.Icon image = gmaps.Icon()
      ..url = 'assets/images/cab-icon-2.png'
      ..scaledSize = gmaps.Size(26, 52);

    for (List<num?> latLng in NearbyCabsLoc.nearbyCabs) {
      gmaps.Marker _cabMarker = gmaps.Marker(gmaps.MarkerOptions()
        ..draggable = true
        ..position = gmaps.LatLng(latLng[0], latLng[1])
        ..icon = image
        ..map = _map);
    }

    /*_sourceMarker.onDragend.listen((event) {
      ComService.startLatLng.add(event.latLng!);
      directionUpdate();
    });

    _destMarker.onDragend.listen((event) {
      ComService.destLatLng.add(event.latLng!);
      directionUpdate();
    });*/

    gmaps.DirectionsRendererOptions direcRendOptions = gmaps.DirectionsRendererOptions()
      ..draggable = false;

    _directionsRenderer = gmaps.DirectionsRenderer()
      ..map = _map
      ..options = direcRendOptions;
    _directionsService = gmaps.DirectionsService();

    directionUpdate();
  }

  void directionUpdate() {
    _directionsService
        .route(gmaps.DirectionsRequest()
          ..origin = _sourceLatLng
          ..destination = _destLatLng
          ..travelMode = gmaps.TravelMode.DRIVING)
        .then((response) => {_directionsRenderer..directions = response});
  }
}
