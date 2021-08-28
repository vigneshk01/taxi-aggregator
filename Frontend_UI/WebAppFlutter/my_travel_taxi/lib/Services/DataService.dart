import 'dart:convert';

import 'package:http/http.dart' as http;

class DataService {
  static final String backendUri = 'https://<www.domain-name.com>/api/';

  static final List<String> pathList = List.of({
    'user/login',
    'user/signup',
    'user/get_nearby_rides',
    'user/get_user_details',
    'user/change_user_details',
    'user/remove_user',
    'ride/request_ride',
    'ride/get_ride_details',
    'ride/confirm_ride',
  });

  static Future<http.Response> postReq(String data, int index) async {
    return http.post(
      Uri.parse(backendUri + pathList[index]),
      headers: <String, String>{
        'Content-Type': 'application/json; charset=UTF-8',
      },
      body: jsonEncode(<String, String>{
        'data': data,
      }),
    );
  }

  static Future<http.Response> getReq(String title, int index) {
    return http.get(
      Uri.parse(backendUri + pathList[index]),
      headers: <String, String>{
        'Content-Type': 'application/json; charset=UTF-8',
      }
    );
  }
}
