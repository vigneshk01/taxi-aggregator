import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:my_travel_taxi/Services/ComService.dart';

class BookedState extends StatefulWidget {
  @override
  _BookedStateState createState() => _BookedStateState();
}

class _BookedStateState extends State<BookedState> {
  @override
  Widget build(BuildContext context) {
    return Column(
      mainAxisAlignment: MainAxisAlignment.start,
      crossAxisAlignment: CrossAxisAlignment.center,
      children: [
        Padding(
          padding: EdgeInsets.fromLTRB(14, 20, 20, 5),
          child: Text(
            'From:',
            style: TextStyle(color: Colors.pink, fontSize: 14),
          ),
        ),
        Padding(
          padding: EdgeInsets.fromLTRB(14, 0, 20, 5),
          child: Text(
            ComService.myRide.value.startAddress,
            textAlign: TextAlign.center,
            style: TextStyle(fontSize: 14),
          ),
        ),
        Padding(
          padding: EdgeInsets.fromLTRB(14, 20, 20, 5),
          child: Text(
            'To:',
            style: TextStyle(color: Colors.pink, fontSize: 14),
          ),
        ),
        Padding(
          padding: EdgeInsets.fromLTRB(14, 0, 20, 5),
          child: Text(
            ComService.myRide.value.destAddress,
            textAlign: TextAlign.center,
            style: TextStyle(fontSize: 14),
          ),
        ),
        Padding(
          padding: EdgeInsets.fromLTRB(14, 20, 20, 5),
          child: Text(
            'Booked Time:',
            style: TextStyle(color: Colors.pink, fontSize: 14),
          ),
        ),
        Padding(
          padding: EdgeInsets.fromLTRB(14, 0, 20, 5),
          child: Text(
            ComService.myRide.value.bookedTime,
            style: TextStyle(fontSize: 14),
          ),
        ),
        Padding(
          padding: EdgeInsets.fromLTRB(14, 20, 20, 5),
          child: Text(
            'Start Time:',
            style: TextStyle(color: Colors.pink, fontSize: 14),
          ),
        ),
        Padding(
          padding: EdgeInsets.fromLTRB(14, 0, 20, 5),
          child: Text(
            ComService.myRide.value.startTime,
            style: TextStyle(fontSize: 14),
          ),
        ),
        Padding(
          padding: EdgeInsets.fromLTRB(14, 20, 20, 5),
          child: Text(
            'End Time:',
            style: TextStyle(color: Colors.pink, fontSize: 14),
          ),
        ),
        Padding(
          padding: EdgeInsets.fromLTRB(14, 0, 20, 5),
          child: Text(
            ComService.myRide.value.endTime,
            style: TextStyle(fontSize: 14),
          ),
        ),
        Padding(
          padding: EdgeInsets.fromLTRB(14, 20, 20, 5),
          child: Text(
            'Ride Status:',
            style: TextStyle(color: Colors.pink, fontSize: 14),
          ),
        ),
        Padding(
          padding: EdgeInsets.fromLTRB(14, 0, 20, 5),
          child: Text(
            ComService.myRide.value.status,
            style: TextStyle(fontSize: 14),
          ),
        ),
      ],
    );
  }
}
