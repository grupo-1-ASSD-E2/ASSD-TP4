import 'dart:math';
import 'dart:typed_data';

import 'package:flutter/material.dart';
import 'dart:async';

import 'package:ffi_google_oboe/ffi_google_oboe.dart';
// import 'package:flutter/services.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatefulWidget {
  @override
  _MyAppState createState() => _MyAppState();
}

class _MyAppState extends State<MyApp> {
  final stream = OboeStream();

  final noise = Float32List(512);
  Timer t;

  @override
  void initState() {
    super.initState();
    for (var i = 0; i < noise.length; i++) {
      noise[i] = sin(8 * pi * 1 / noise.length);
    }
  }

  // // Platform messages are asynchronous, so we initialize in an async method.
  // Future<void> initPlatformState() async {
  //   String platformVersion;
  //   // Platform messages may fail, so we use a try/catch PlatformException.
  //   try {
  //     platformVersion = await FfiGoogleOboe.platformVersion;
  //   } on PlatformException {
  //     platformVersion = 'Failed to get platform version.';
  //   }

  //   // If the widget was removed from the tree while the asynchronous platform
  //   // message was in flight, we want to discard the reply rather than calling
  //   // setState to update our non-existent appearance.
  //   if (!mounted) return;

  //   setState(() {
  //     _platformVersion = platformVersion;
  //   });
  // }

  @override
  void dispose() {
    stream.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
        appBar: AppBar(
          title: const Text('Plugin example app'),
        ),
        body: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: <Widget>[
              Text('Running at: ${stream.getSampleRate()}\n'),
              RaisedButton(
                child: Text('START'),
                onPressed: start,
              ),
              RaisedButton(
                child: Text('STOP'),
                onPressed: stop,
              ),
            ],
          ),
        ),
      ),
    );
  }

  void start() {
    stream.start();
    var interval = (512000 / stream.getSampleRate()).floor() + 1;
    t = Timer.periodic(Duration(milliseconds: interval), (_) {
      stream.write(noise);
     });
  }

  void stop() {
    t?.cancel();
    t = null;
    stream.stop();
  }
}
