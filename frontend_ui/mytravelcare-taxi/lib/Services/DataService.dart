
import 'package:http/http.dart' as http;
import 'package:my_travel_taxi/Data/checker.dart';

class DataService {
  final String? _backendUri = Checker.checkMap['apiURI'];

  final List<String> _pathList = List.of({
    '/api/rides/confirmride',
    '/api/rides/getaride',
    '/api/ridesearch/getnearbyrides',
    '/api/users/getuser',
    '/api/users/login',
    '/api/users/newuser',
    '/api/users/removeuser',
    '/api/rides/updateride',
    '/api/rides/getridelocation',
    '/alltaxis',
    '/api/taxi/getcurrenttaxidata',
    '/api/users/getridehistory'
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

  Future<http.Response> getReq(int index) {
    return http.get(
      Uri.parse(_backendUri! + _pathList[index]),
      headers: <String, String>{
        'Content-Type': 'application/json'
      }
    );
  }
}
