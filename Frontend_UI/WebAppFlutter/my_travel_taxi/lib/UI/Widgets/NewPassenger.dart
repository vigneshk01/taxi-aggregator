import 'package:flutter/material.dart';

class NewPassenger extends StatefulWidget {
  const NewPassenger({Key? key}) : super(key: key);

  @override
  _NewPassengerState createState() => _NewPassengerState();
}

class _NewPassengerState extends State<NewPassenger> {
  GlobalKey _key = GlobalKey<FormState>();

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
                      Navigator.pushNamed(context, '/login');
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
                        Navigator.pushNamed(context, '/mapview');
                      },
                      child: Text("Create"))),
            ],
          ),
        ),
      ),
    );
  }
}
