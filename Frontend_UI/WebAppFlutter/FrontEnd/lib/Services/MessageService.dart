import 'package:flutter/material.dart';

class MessageService {
  static showMessage(BuildContext context, String message, Color color) {
    final snackBar = SnackBar(
      elevation: 5,
      backgroundColor: color,
      content: Container(
        height: 35,
        alignment: Alignment.center,
        child: Text(message),
      ),
    );
    ScaffoldMessenger.of(context).showSnackBar(snackBar);
  }
}
