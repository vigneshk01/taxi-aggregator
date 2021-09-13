
import 'package:http/http.dart' as http;
import 'package:my_travel_taxi/Data/checker.dart';

class DataService {
  final String? _backendUri = Checker.checkMap['apiURI']!+'/api/';

  final List<String> _pathList = List.of({
    'rides/confirmride',
    'rides/getaride',
    'ridesearch/getnearbyrides',
    'users/getuser',
    'users/login',
    'users/newuser',
    'users/removeuser',
    'rides/updateride',
    'rides/getridelocation'
  });

  Future<http.Response> postReq(Object data, int index) {
    String url = _backendUri! + _pathList[index];
    return http.post(
      Uri.parse(url),
      headers: {
        'Content-Type': 'application/json'
      },
      body: data,
    );
  }

  Future<http.Response> getReq(String title, int index) {
    return http.get(
      Uri.parse(_backendUri! + _pathList[index]),
      headers: <String, String>{
        'Content-Type': 'application/json'
      }
    );
  }
}
