import 'package:flutter/material.dart';

class MessageService {
  static showMessage(BuildContext context, String message, Color color) {
    final snackBar = SnackBar(
      elevation: 5,
      behavior: SnackBarBehavior.floating,
      width: 300,
      backgroundColor: color,
      duration: Duration(seconds: 2),
      content: Container(
        height: 35,
        alignment: Alignment.center,
        child: Text(message),
      ),
    );
    ScaffoldMessenger.of(context).showSnackBar(snackBar);
  }
}
