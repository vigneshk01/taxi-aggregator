import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';

class RideItem extends StatefulWidget {
  const RideItem(
      {Key? key,
      required this.from,
      required this.to,
      required this.startLoc,
      required this.endLoc,
      required this.bookedTime,
      required this.startTime,
      required this.endTime,
      required this.vehicleType,
      required this.vehicleNum,
      required this.cost,
      required this.passengerRating,
      required this.passengerComments,
      required this.estTime,
      required this.totalDist,
      required this.status})
      : super(key: key);

  final String from, to, startLoc, endLoc;
  final String bookedTime, startTime, endTime;
  final String vehicleType, vehicleNum, cost;
  final String passengerRating, passengerComments;
  final String estTime, totalDist, status;

  @override
  _RideItemState createState() => _RideItemState();
}

class _RideItemState extends State<RideItem> {
  @override
  Widget build(BuildContext context) {
    return Card(
      child: Padding(
        padding: EdgeInsets.all(20),
        child: Column(
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              crossAxisAlignment: CrossAxisAlignment.center,
              children: [
                Container(
                  width: 100,
                  child: Text(
                    "From: ",
                    style: TextStyle(color: Colors.pink),
                  ),
                ),
                Container(
                  width: 300,
                  child: Text(widget.from),
                ),
              ],
            ),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              crossAxisAlignment: CrossAxisAlignment.center,
              children: [
                Container(
                  width: 100,
                  child: Text(
                    "To: ",
                    style: TextStyle(color: Colors.pink),
                  ),
                ),
                Container(
                  width: 300,
                  child: Text(widget.to),
                ),
              ],
            ),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              crossAxisAlignment: CrossAxisAlignment.center,
              children: [
                Container(
                  width: 100,
                  child: Text(
                    "Start Location: ",
                    style: TextStyle(color: Colors.pink),
                  ),
                ),
                Container(width: 300, child: Text(widget.startLoc))
              ],
            ),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              crossAxisAlignment: CrossAxisAlignment.center,
              children: [
                Container(
                  width: 100,
                  child: Text(
                    "End Location: ",
                    style: TextStyle(color: Colors.pink),
                  ),
                ),
                Container(width: 300, child: Text(widget.endLoc)),
              ],
            ),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              crossAxisAlignment: CrossAxisAlignment.center,
              children: [
                Container(
                  width: 100,
                  child: Text(
                    "Booked time: ",
                    style: TextStyle(color: Colors.pink),
                  ),
                ),
                Container(width: 300, child: Text(widget.bookedTime)),
              ],
            ),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              crossAxisAlignment: CrossAxisAlignment.center,
              children: [
                Container(
                  width: 100,
                  child: Text(
                    "Start time: ",
                    style: TextStyle(color: Colors.pink),
                  ),
                ),
                Container(
                  width: 300,
                  child: Text(widget.startTime),
                ),
              ],
            ),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              crossAxisAlignment: CrossAxisAlignment.center,
              children: [
                Container(
                  width: 100,
                  child: Text(
                    "End time: ",
                    style: TextStyle(color: Colors.pink),
                  ),
                ),
                Container(
                  width: 300,
                  child: Text(widget.endTime),
                ),
              ],
            ),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              crossAxisAlignment: CrossAxisAlignment.center,
              children: [
                Container(
                  width: 100,
                  child: Text(
                    "Vehicle type: ",
                    style: TextStyle(color: Colors.pink),
                  ),
                ),
                Container(
                  width: 300,
                  child: Text(widget.vehicleType),
                ),
              ],
            ),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              crossAxisAlignment: CrossAxisAlignment.center,
              children: [
                Container(
                  width: 100,
                  child: Text(
                    "Vehicle number: ",
                    style: TextStyle(color: Colors.pink),
                  ),
                ),
                Container(
                  width: 300,
                  child: Text(widget.vehicleNum),
                ),
              ],
            ),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              crossAxisAlignment: CrossAxisAlignment.center,
              children: [
                Container(
                  width: 100,
                  child: Text(
                    "Cost: ",
                    style: TextStyle(color: Colors.pink),
                  ),
                ),
                Container(
                  width: 300,
                  child: Text(widget.cost),
                ),
              ],
            ),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              crossAxisAlignment: CrossAxisAlignment.center,
              children: [
                Container(
                  width: 100,
                  child: Text(
                    "Passenger rating: ",
                    style: TextStyle(color: Colors.pink),
                  ),
                ),
                Container(
                  width: 300,
                  child: Text(widget.passengerRating),
                ),
              ],
            ),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              crossAxisAlignment: CrossAxisAlignment.center,
              children: [
                Container(
                  width: 100,
                  child: Text(
                    "Passenger comments: ",
                    style: TextStyle(color: Colors.pink),
                  ),
                ),
                Container(
                  width: 300,
                  child: Text(widget.passengerComments),
                ),
              ],
            ),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              crossAxisAlignment: CrossAxisAlignment.center,
              children: [
                Container(
                  width: 100,
                  child: Text(
                    "Estimated time: ",
                    style: TextStyle(color: Colors.pink),
                  ),
                ),
                Container(
                  width: 300,
                  child: Text(widget.estTime),
                ),
              ],
            ),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              crossAxisAlignment: CrossAxisAlignment.center,
              children: [
                Container(
                  width: 100,
                  child: Text(
                    "Total distance: ",
                    style: TextStyle(color: Colors.pink),
                  ),
                ),
                Container(
                  width: 300,
                  child: Text(widget.totalDist),
                ),
              ],
            ),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              crossAxisAlignment: CrossAxisAlignment.center,
              children: [
                Container(
                  width: 100,
                  child: Text(
                    "Status: ",
                    style: TextStyle(color: Colors.pink),
                  ),
                ),
                Container(
                  width: 300,
                  child: Text(widget.status),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
