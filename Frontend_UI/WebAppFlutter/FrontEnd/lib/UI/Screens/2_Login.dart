import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:http/http.dart';
import 'package:my_travel_taxi/Models/PathsEnum.dart';
import 'package:my_travel_taxi/Services/ComService.dart';
import 'package:my_travel_taxi/Services/DataService.dart';
import 'package:crypto/crypto.dart';
import 'dart:convert';

import 'package:my_travel_taxi/Services/MessageService.dart';

class Login extends StatefulWidget {
  const Login({Key? key}) : super(key: key);

  @override
  _LoginState createState() => _LoginState();
}

class _LoginState extends State<Login> {

  final GlobalKey<FormState> _key = GlobalKey<FormState>();

  late String _username;
  late String _password;
  late String _userType;
  late bool _onEnterPending;

  @override
  void initState() {
    super.initState();
    _username = '';
    _password = '';
    _userType = 'Passenger';
    _onEnterPending = false;
  }

  @override
  Widget build(BuildContext context) {

    return Scaffold(
      appBar: AppBar(
        title: Text("Login"),
        centerTitle: true,
      ),
      body: Stack(children: [
        SingleChildScrollView(
          child: Center(
            child: Form(
              key: _key,
              child: Column(
                children: [
                  Padding(
                      padding: EdgeInsets.all(20),
                      child: TextButton(
                        child: Text("Go to Create Account"),
                        onPressed: () {
                          Navigator.pushNamed(context, '/signup');
                        },
                      )),
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
                          setState(() {
                            _username = newVal!;
                          });
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
                          hintText: "password",
                          filled: true,
                          fillColor: Colors.white,
                        ),
                        validator: (value) {
                          if (value == null || value.isEmpty) {
                            return 'Please enter password';
                          }
                          return null;
                        },
                        onSaved: (newVal) {
                          setState(() {
                            _password = newVal!;
                          });
                        },
                      ),
                    ),
                  ),
                  Padding(
                    padding: EdgeInsets.all(20),
                    child: Container(
                      width: 300,
                      color: Colors.white,
                      child: DropdownButton(
                        value: _userType,
                        onChanged: (String? newVal) {
                          setState(() {
                            _userType = newVal!;
                          });
                        },
                        items: <String>["Passenger", "Taxi"]
                            .map<DropdownMenuItem<String>>((String value) {
                          return DropdownMenuItem<String>(
                            value: value,
                            child: Container(
                              alignment: Alignment.center,
                              width: 276,
                                color: Colors.white,
                                child: Text(value),
                            ),
                          );
                        }).toList()),),
                  ),
                  Padding(
                      padding: EdgeInsets.all(20),
                      child: ElevatedButton(
                          onPressed: () {
                            setState(() {
                              _onEnterPending = true;
                            });
                            if (_key.currentState!.validate()) {
                              _key.currentState!.save();
                              _onEnterPressed().then((response) {
                                setState(() {
                                  _onEnterPending = false;
                                });
                                if (response.statusCode == 200) {
                                  final Map<String, dynamic> body = json.decode(response.body);
                                  ComService.apiKey.add(body['APIKey']);
                                  MessageService.showMessage(context,
                                      "Login Successful!", Colors.green);
                                  Navigator.pushReplacementNamed(context, '/routeview');
                                } else {
                                  MessageService.showMessage(
                                      context, "Login Failed!", Colors.red);
                                }
                              }, onError: (_) {
                                MessageService.showMessage(
                                    context, "Login Failed!", Colors.red);
                              });
                            }
                            else {
                              setState(() {
                                _onEnterPending = false;
                              });
                            }
                          },
                          child: Text("Enter"))),
                ],
              ),
            ),
          ),
        ),
        Visibility(
          visible: _onEnterPending,
          child: LinearProgressIndicator(),
        )
      ]),
    );
  }

  Future<Response> _onEnterPressed() {
    String usernameHash = sha256.convert(_username.codeUnits).toString();
    String passwordHash = sha256.convert(_password.codeUnits).toString();
    Map<String, String> data = {
      "username": usernameHash,
      "password": passwordHash,
      "user_type": _userType
    };

    return DataService()
        .postReq(JsonEncoder().convert(data), APIPaths.Login.index);
  }
}
