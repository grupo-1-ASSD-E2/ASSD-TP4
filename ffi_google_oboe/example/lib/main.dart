import 'dart:math';
import 'dart:typed_data';

import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'dart:async';
import 'package:path_provider/path_provider.dart';
import 'package:audioplayer/audioplayer.dart';
import 'dart:io';

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

  var noise = Uint8List(512);
  Timer t;

  @override
  void initState() {
    super.initState();
    // for (var i = 0; i < noise.length; i++) {
    //   noise[i] = sin(8 * pi * i / noise.length);
    // }
    
    _loadSound();
  }

  void _loadSound() async {
    final ByteData data = await rootBundle.load('assets/queen_bohemian_rhapsody_cut.wav');
    noise = data.buffer.asUint8List();
  }

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
