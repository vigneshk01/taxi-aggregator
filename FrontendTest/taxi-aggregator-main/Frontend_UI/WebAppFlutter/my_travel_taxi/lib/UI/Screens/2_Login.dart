import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:my_travel_taxi/Models/PathsEnum.dart';
import 'package:my_travel_taxi/Services/DataService.dart';

class Login extends StatefulWidget {
  const Login({Key? key}) : super(key: key);

  @override
  _LoginState createState() => _LoginState();
}

class _LoginState extends State<Login> {
  String? userType = 'Passenger';

  GlobalKey _key = GlobalKey<FormState>();
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("Login"),
        centerTitle: true,
      ),
      body: SingleChildScrollView(
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
                    ),
                  ),
                ),
                Padding(
                  padding: EdgeInsets.all(20),
                  child: DropdownButton(
                      value: userType,
                      onChanged: (String? newval) {
                        setState(() {
                          userType = newval;
                        });
                      },
                      style: TextStyle(color: Colors.pink),
                      items: <String>["Passenger", "Driver"]
                          .map<DropdownMenuItem<String>>((String value) {
                        return DropdownMenuItem<String>(
                          value: value,
                          child: Text(value),
                        );
                      }).toList()),
                ),
                Padding(
                    padding: EdgeInsets.all(20),
                    child: ElevatedButton(
                        onPressed: () {
                          Navigator.pushNamed(context, '/mapview');
                        },
                        child: Text("Enter"))),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
