import 'package:flutter/material.dart';
import 'dart:html';
import 'package:google_maps/google_maps.dart' as gmaps;
import 'dart:ui' as ui;
import 'package:google_maps/google_maps_places.dart';
import 'package:my_travel_taxi/Data/Nearby-Cabs-Loc.dart';
import 'package:my_travel_taxi/Models/FetchDetails.dart';
// import 'package:razorpay_flutter/razorpay_flutter.dart';

class MapView extends StatefulWidget {
  @override
  _MapViewState createState() => _MapViewState();
}

class _MapViewState extends State<MapView> {
  late List<FetchDetails> triplist = [
    FetchDetails('Luxury', '1-2', 'Select sedans, top-rated drivers',
        'Available', 270.56)
  ];
  late num? sourceLat, sourceLong;
  late num? destLat, destLong;
  late num? cabLat, cabLong;
  late String? vehicleType, eta;

  late final gmaps.MapRestriction mapRestrictions;
  late final gmaps.MapOptions mapOptions;
  late final DivElement elem;
  late final gmaps.GMap map;
  late final gmaps.Marker sourceMarker, destMarker;
  late gmaps.Marker cabMarker;

  late final gmaps.DirectionsRenderer directionsRenderer;
  late final gmaps.DirectionsService directionsService;

  late gmaps.Polyline poly;
  late gmaps.Polyline geodesicPoly;

  late gmaps.LatLng myLatLng, destLatLng;

  // late Razorpay _razorpay;

  @override
  void initState() {
    super.initState();
    sourceLat = 12.9788427;
    sourceLong = 77.5974611;
    destLat = 12.9788027;
    destLong = 77.5974211;

    myLatLng = gmaps.LatLng(sourceLat, sourceLong);
    destLatLng = gmaps.LatLng(destLat, destLong);

    // _razorpay = new Razorpay();
    // _razorpay.on(Razorpay.EVENT_PAYMENT_SUCCESS, handlePaymentSuccess);
    // _razorpay.on(Razorpay.EVENT_PAYMENT_ERROR, handlePaymentError);
    // _razorpay.on(Razorpay.EVENT_EXTERNAL_WALLET, handleExternalWallet);

    vehicleType = 'Deluxe';
    eta = 'sometime now';
  }

  // @override
  // void dispose() {
  //   super.dispose();
  //   _razorpay.clear(); // Removes all listeners
  // }

  // void openCheckout() async {
  //   var options = {
  //     'key': 'rzp_live_ILgsfZCZoFIKMb',
  //     'amount': 100,
  //     'name': 'Acme Corp.',
  //     "id": "order_HuIev5rwxB18Db",
  //     'description': 'Fine T-Shirt',
  //     'timeout': 60,
  //     'prefill': {'contact': '8888888888', 'email': 'test@razorpay.com'},
  //     'external': {
  //       'wallets': ['paytm']
  //     }
  //   };
  //   try {
  //     _razorpay.open(options);
  //   } catch (e) {
  //     print("Inside error");
  //     print(e.toString());
  //   }
  // }

  // void handlePaymentSuccess(PaymentSuccessResponse response) {
  //   // Do something when payment succeeds}
  //   print("payment success");
  // }

  // void handlePaymentError(PaymentFailureResponse response) {
  //   // Do something when payment fails}
  //   print("Payment error");
  // }

  // void handleExternalWallet(ExternalWalletResponse response) {
  //   // Do something when an external wallet is selected}
  //   print("External wallet");
  // }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        appBar: AppBar(
          title: Text('Select Transit Route'),
        ),
        drawer: Container(
            color: Colors.white,
            width: 250,
            child: SingleChildScrollView(
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
                            child: Icon(Icons.location_on,
                                color: Colors.green, size: 18),
                          ),
                          Text(
                            'Start Location',
                            style: TextStyle(color: Colors.pink, fontSize: 18),
                          ),
                        ]),
                  ),
                  Padding(
                    padding: EdgeInsets.fromLTRB(18, 0, 20, 4),
                    child: Text('latitude: ' + sourceLat.toString(),
                        style: TextStyle(color: Colors.pink, fontSize: 12)),
                  ),
                  Padding(
                    padding: EdgeInsets.fromLTRB(18, 0, 20, 20),
                    child: Text('longitude: ' + sourceLong.toString(),
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
                            child: Icon(Icons.location_on,
                                color: Colors.blue, size: 18),
                          ),
                          Text(
                            'End Location',
                            style: TextStyle(color: Colors.pink, fontSize: 18),
                          ),
                        ]),
                  ),
                  Padding(
                    padding: EdgeInsets.fromLTRB(18, 0, 20, 4),
                    child: Text('latitude: ' + destLat.toString(),
                        style: TextStyle(color: Colors.pink, fontSize: 12)),
                  ),
                  Padding(
                    padding: EdgeInsets.fromLTRB(18, 0, 20, 20),
                    child: Text('longitude: ' + destLong.toString(),
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
                              value: vehicleType,
                              onChanged: (String? newval) {
                                setState(() {
                                  vehicleType = newval;
                                });
                              },
                              style: TextStyle(color: Colors.pink),
                              items: <String>[
                                "Utility",
                                "Deluxe",
                                "Luxury"
                              ].map<DropdownMenuItem<String>>((String value) {
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
                              value: eta,
                              onChanged: (String? newval) {
                                setState(() {
                                  eta = newval;
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
                  Container(
                      height: double.maxFinite,
                      child: ListView.builder(
                          itemCount: triplist == null ? 0 : triplist.length,
                          itemBuilder: (BuildContext context, i) {
                            return Card(
                              child: Column(
                                children: [
                                  InkWell(
                                    splashColor: Colors.blue.withAlpha(30),
                                    onTap: () {
                                      if (triplist[i].status == 'Unavailable') {
                                        final snackBar = SnackBar(
                                          content: const Text(
                                            'Ride is unavailable',
                                            textAlign: TextAlign.center,
                                          ),
                                          action: SnackBarAction(
                                            label: 'Undo',
                                            onPressed: () {
                                              //some code to do
                                            },
                                          ),
                                        );

                                        // Find the ScaffoldMessenger in the widget tree
                                        // and use it to show a SnackBar.
                                        ScaffoldMessenger.of(context)
                                            .showSnackBar(snackBar);
                                        print('Card tapped.');
                                      } else {
                                        // openCheckout();
                                      }
                                    },
                                    child: Column(
                                      children: [
                                        ListTile(
                                          leading: Icon(Icons.car_rental),
                                          title: Text(triplist[i].rideType),
                                          subtitle: Text(triplist[i].details),
                                        ),
                                        SizedBox(height: 10),
                                        ListTile(
                                          title: Text(triplist[i].status),
                                        ),
                                        SizedBox(height: 20),
                                        Row(
                                          children: [
                                            SizedBox(width: 10),
                                            Icon(Icons.people),
                                            Text(triplist[i].capacity),
                                            SizedBox(width: 10),
                                            Icon(Icons.money),
                                            Text(triplist[i]
                                                .tripCost
                                                .toString()),
                                            const SizedBox(width: 8),
                                          ],
                                        ),
                                      ],
                                    ),
                                  ),
                                ],
                              ),
                            );
                          }))
                ],
              ),
            )),
        body: mapWidget());
  }

  Widget mapWidget() {
    String htmlId = "mapView";

    // ignore: undefined_prefixed_name
    ui.platformViewRegistry.registerViewFactory(htmlId, (int viewId) {
      final sw = gmaps.LatLng(12.863035, 77.429122);
      final ne = gmaps.LatLng(13.0054049, 77.6904627);

      mapRestrictions = gmaps.MapRestriction()
        ..latLngBounds = gmaps.LatLngBounds(sw, ne);

      mapOptions = gmaps.MapOptions()
        ..zoom = 15
        ..center = gmaps.LatLng(12.9788427, 77.5974611)
        ..mapTypeControl = true
        ..mapTypeControlOptions = (gmaps.MapTypeControlOptions()
          ..style = gmaps.MapTypeControlStyle.DEFAULT
          ..position = gmaps.ControlPosition.BOTTOM_RIGHT)
        ..restriction = mapRestrictions;

      elem = DivElement()
        ..id = htmlId
        ..style.width = "100%"
        ..style.height = "100%"
        ..style.border = 'none';

      map = gmaps.GMap(elem, mapOptions);

      sourceMarker = gmaps.Marker(gmaps.MarkerOptions()
        ..draggable = true
        ..position = myLatLng
        ..icon = (gmaps.GSymbol()
          ..path = gmaps.SymbolPath.FORWARD_CLOSED_ARROW
          ..fillColor = 'green'
          ..fillOpacity = 1
          ..strokeColor = 'green'
          ..strokeOpacity = 1
          ..strokeWeight = 3
          ..scale = 6)
        ..map = map
        ..label = 'Start location');

      destMarker = gmaps.Marker(gmaps.MarkerOptions()
        ..draggable = true
        ..position = destLatLng
        ..icon = (gmaps.GSymbol()
          ..path = gmaps.SymbolPath.FORWARD_CLOSED_ARROW
          ..fillColor = 'blue'
          ..fillOpacity = 1
          ..strokeColor = 'blue'
          ..strokeOpacity = 1
          ..strokeWeight = 3
          ..scale = 6)
        ..map = map
        ..label = 'Destination location');

      final image = gmaps.Icon()
        ..url = 'assets/images/cab-icon-2.png'
        ..scaledSize = gmaps.Size(30, 60);

      for (List<num?> latLng in NearbyCabsLoc.nearbyCabs) {
        cabMarker = gmaps.Marker(gmaps.MarkerOptions()
          ..draggable = true
          ..position = gmaps.LatLng(latLng[0], latLng[1])
          ..icon = image
          ..map = map);
      }

      sourceMarker.onDragend.listen((event) {
        setState(() {
          sourceLat = event.latLng!.lat;
          sourceLong = event.latLng!.lng;
        });
        directionUpdate();
      });

      destMarker.onDragend.listen((event) {
        setState(() {
          destLat = event.latLng!.lat;
          destLong = event.latLng!.lng;
        });
        directionUpdate();
      });

      final direcRendOptions = gmaps.DirectionsRendererOptions()
        ..draggable = false;

      directionsRenderer = gmaps.DirectionsRenderer()
        ..map = map
        ..options = direcRendOptions;
      directionsService = gmaps.DirectionsService();

      directionUpdate();

      return elem;
    });

    return HtmlElementView(viewType: htmlId);
  }

  void directionUpdate() {
    directionsService
        .route(gmaps.DirectionsRequest()
          ..origin = sourceMarker.position
          ..destination = destMarker.position
          ..travelMode = gmaps.TravelMode.DRIVING)
        .then((response) => {directionsRenderer..directions = response});
  }
}
