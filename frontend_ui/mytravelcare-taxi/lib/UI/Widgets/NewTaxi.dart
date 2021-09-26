import 'dart:convert';

import 'package:crypto/crypto.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:http/http.dart';
import 'package:my_travel_taxi/Models/PathsEnum.dart';
import 'package:my_travel_taxi/Services/DataService.dart';
import 'package:my_travel_taxi/Services/MessageService.dart';

class NewTaxi extends StatefulWidget {
  const NewTaxi({Key? key}) : super(key: key);

  @override
  _NewTaxiState createState() => _NewTaxiState();
}

class _NewTaxiState extends State<NewTaxi> {
  final GlobalKey<FormState> _key = GlobalKey<FormState>();

  late String _firstname;
  late String _lastname;
  late String _username;
  late String _password;
  late String _vehicleNum;
  late String _vehicleType;
  late String _drivingLicenseNum;
  late double _lat, _lng;
  late String _status;
  late String _userType;
  late bool _onCreatePending;

  @override
  void initState() {
    super.initState();
    _firstname = '';
    _lastname = '';
    _username = '';
    _password = '';
    _vehicleNum = '';
    _vehicleType = 'UTILITY';
    _drivingLicenseNum = '';
    _lat = 0;
    _lng = 0;
    _status = 'INACTIVE';
    _userType = 'Taxi';
    _onCreatePending = false;
  }

  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      child: Center(
        child: Form(
          key: _key,
          child: Column(
            children: [
              Padding(
                  padding: EdgeInsets.all(20),
                  child: TextButton(
                    child: Text("Go to Login"),
                    onPressed: () {
                      Navigator.pop(context);
                    },
                  )),
              Flex(
                direction: Axis.horizontal,
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Padding(
                    padding: EdgeInsets.all(20),
                    child: Container(
                      width: 300,
                      child: TextFormField(
                        textAlign: TextAlign.center,
                        decoration: InputDecoration(
                            hintText: "first name",
                            filled: true,
                            fillColor: Colors.white),
                        validator: (value) {
                          if (value == null || value.isEmpty) {
                            return 'Please enter first name';
                          }
                          return null;
                        },
                        onSaved: (newVal) {
                          _firstname = newVal!;
                        },
                      ),
                    ),
                  ),
                  Padding(
                    padding: EdgeInsets.all(20),
                    child: Container(
                      width: 300,
                      child: TextFormField(
                        textAlign: TextAlign.center,
                        decoration: InputDecoration(
                            hintText: "last name",
                            filled: true,
                            fillColor: Colors.white),
                        validator: (value) {
                          if (value == null || value.isEmpty) {
                            return 'Please enter last name';
                          }
                          return null;
                        },
                        onSaved: (newVal) {
                          _lastname = newVal!;
                        },
                      ),
                    ),
                  ),
                ],
              ),
              Flex(
                direction: Axis.horizontal,
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Padding(
                    padding: EdgeInsets.all(20),
                    child: Container(
                      width: 300,
                      child: TextFormField(
                        textAlign: TextAlign.center,
                        decoration: InputDecoration(
                            hintText: "vehicle number on number plate",
                            filled: true,
                            fillColor: Colors.white),
                        validator: (value) {
                          if (value == null || value.isEmpty) {
                            return 'Please enter vehicle number';
                          }
                          return null;
                        },
                        onSaved: (newVal) {
                          _vehicleNum = newVal!;
                        },
                      ),
                    ),
                  ),
                  Padding(
                    padding: EdgeInsets.all(20),
                    child: Container(
                      width: 300,
                      child: TextFormField(
                        textAlign: TextAlign.center,
                        decoration: InputDecoration(
                            hintText: "driving license number",
                            filled: true,
                            fillColor: Colors.white),
                        validator: (value) {
                          if (value == null || value.isEmpty) {
                            return 'Please enter driving license number';
                          }
                          return null;
                        },
                        onSaved: (newVal) {
                          _drivingLicenseNum = newVal!;
                        },
                      ),
                    ),
                  ),
                ],
              ),
              Flex(
                direction: Axis.horizontal,
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Padding(
                    padding: EdgeInsets.all(20),
                    child: Container(
                      width: 300,
                      color: Colors.white,
                      child: DropdownButton(
                        value: _vehicleType,
                        onChanged: (String? newval) {
                          if (mounted) {
                            setState(() {
                              _vehicleType = newval!;
                            });
                          }
                        },
                        style: TextStyle(backgroundColor: Colors.white),
                        items: <String>["UTILITY", "DELUXE", "LUXURY"]
                            .map<DropdownMenuItem<String>>((String value) {
                          return DropdownMenuItem<String>(
                            value: value,
                            child: Container(
                              width: 276,
                              alignment: Alignment.center,
                              child: Text(value),
                            ),
                          );
                        }).toList(),
                      ),
                    ),
                  ),
                  Padding(
                    padding: EdgeInsets.all(20),
                    child: Container(
                      color: Colors.white,
                      width: 300,
                      child: DropdownButton(
                        value: _status,
                        onChanged: (String? newval) {
                          if (mounted) {
                            setState(() {
                              _status = newval!;
                            });
                          }
                        },
                        items: <String>["INACTIVE", "ACTIVE"]
                            .map<DropdownMenuItem<String>>((String value) {
                          return DropdownMenuItem<String>(
                            value: value,
                            child: Container(
                              width: 276,
                              alignment: Alignment.center,
                              child: Text(value),
                            ),
                          );
                        }).toList(),
                      ),
                    ),
                  ),
                ],
              ),
              Padding(
                padding: EdgeInsets.all(20),
                child: Container(
                  width: 300,
                  child: TextFormField(
                    textAlign: TextAlign.center,
                    decoration: InputDecoration(
                        hintText: "username",
                        filled: true,
                        fillColor: Colors.white),
                    validator: (value) {
                      if (value == null || value.isEmpty) {
                        return 'Please enter username';
                      }
                      return null;
                    },
                    onSaved: (newVal) {
                      _username = newVal!;
                    },
                  ),
                ),
              ),
              Flex(
                  direction: Axis.horizontal,
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Padding(
                      padding: EdgeInsets.all(20),
                      child: Container(
                        width: 300,
                        child: TextFormField(
                          obscureText: true,
                          textAlign: TextAlign.center,
                          decoration: InputDecoration(
                              hintText: "password",
                              filled: true,
                              fillColor: Colors.white),
                          validator: (value) {
                            if (value == null || value.isEmpty) {
                              return 'Please enter password';
                            }
                            return null;
                          },
                          onChanged: (newVal) {
                            if (mounted) {
                              setState(() {
                                _password = newVal;
                              });
                            }
                          },
                          onSaved: (newVal) {
                            _password = newVal!;
                          },
                        ),
                      ),
                    ),
                    Padding(
                      padding: EdgeInsets.all(20),
                      child: Container(
                        width: 300,
                        child: TextFormField(
                          obscureText: true,
                          textAlign: TextAlign.center,
                          decoration: InputDecoration(
                              hintText: "re-enter password",
                              filled: true,
                              fillColor: Colors.white),
                          validator: (value) {
                            if (value == null || value.isEmpty) {
                              return 'Please re-enter password';
                            } else if (value != _password) {
                              return 'Confirm password does not match password';
                            }
                            return null;
                          },
                        ),
                      ),
                    ),
                  ]),
              Padding(
                  padding: EdgeInsets.all(20),
                  child: ElevatedButton(
                      onPressed: () {
                        if (mounted) {
                          setState(() {
                            _onCreatePending = true;
                          });
                        }
                        if (_key.currentState!.validate()) {
                          _key.currentState!.save();
                          _onCreatePressed().then((response) {
                            if (mounted) {
                              setState(() {
                                _onCreatePending = false;
                              });
                            }
                            if (response.statusCode == 200) {
                              MessageService.showMessage(
                                  context, "SignUp Successful!", Colors.green);
                              Navigator.pop(context);
                            } else {
                              MessageService.showMessage(
                                  context, "SignUp Failed!", Colors.red);
                            }
                          }, onError: (_) {
                            if (mounted) {
                              setState(() {
                                _onCreatePending = false;
                              });
                            }
                            MessageService.showMessage(
                                context, "SignUp Failed!", Colors.red);
                          });
                        } else {
                          if (mounted) {
                            setState(() {
                              _onCreatePending = false;
                            });
                          }
                        }
                      },
                      child: Text("Create"))),
            ],
          ),
        ),
      ),
    );
  }

  Future<Response> _onCreatePressed() {
    String usernameHash = sha256.convert(_username.codeUnits).toString();
    String passwordHash = sha256.convert(_password.codeUnits).toString();
    var data = {
      "firstname": _firstname,
      "lastname": _lastname,
      "username": usernameHash,
      "password": passwordHash,
      "vehicle_num": _vehicleNum,
      "vehicle_type": _vehicleType,
      "driving_license_num": _drivingLicenseNum,
      "lat": _lat,
      "lng": _lng,
      "status": "ACTIVE",
      "user_type": _userType
    };

    return DataService()
        .postReq(JsonEncoder().convert(data), APIPaths.NewUser.index);
  }
}
