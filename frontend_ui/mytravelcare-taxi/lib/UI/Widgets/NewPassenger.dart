import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:crypto/crypto.dart';
import 'package:http/http.dart';
import 'package:my_travel_taxi/Models/PathsEnum.dart';
import 'package:my_travel_taxi/Services/DataService.dart';
import 'package:my_travel_taxi/Services/MessageService.dart';

class NewPassenger extends StatefulWidget {
  const NewPassenger({Key? key}) : super(key: key);

  @override
  _NewPassengerState createState() => _NewPassengerState();
}

class _NewPassengerState extends State<NewPassenger> {
  final GlobalKey<FormState> _key = GlobalKey<FormState>();

  late String _firstname;
  late String _lastname;
  late String _username;
  late String _password;
  late String _userType;
  late bool _onCreatePending;

  @override
  void initState() {
    super.initState();
    _firstname = '';
    _lastname = '';
    _username = '';
    _password = '';
    _userType = 'Passenger';
    _onCreatePending = false;
  }

  @override
  Widget build(BuildContext context) {
    return Stack(
      children: [
        SingleChildScrollView(
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
                      ]),
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
                                  hintText: "re-enter pasword",
                                  filled: true,
                                  fillColor: Colors.white),
                              validator: (value) {
                                if (value == null || value.isEmpty) {
                                  return 'Please enter password';
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
                      child: Text("Create"),
                    ),
                  ),
                ],
              ),
            ),
          ),
        ),
        Visibility(
          visible: _onCreatePending,
          child: LinearProgressIndicator(),
        ),
      ],
    );
  }

  Future<Response> _onCreatePressed() {
    String usernameHash = sha256.convert(_username.codeUnits).toString();
    String passwordHash = sha256.convert(_password.codeUnits).toString();
    Map<String, String> data = {
      "firstname": _firstname,
      "lastname": _lastname,
      "username": usernameHash,
      "password": passwordHash,
      "user_type": _userType
    };

    return DataService()
        .postReq(JsonEncoder().convert(data), APIPaths.NewUser.index);
  }
}
