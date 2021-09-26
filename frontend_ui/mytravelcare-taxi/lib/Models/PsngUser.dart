class PsngUser {
  String firstname = '' ;
  String lastname = '';

  init() {
    firstname = '';
    lastname = '';
  }

  setFromJSON(Map<String, dynamic> body) {
    firstname = body['firstname'];
    lastname = body['lastname'];
  }
}