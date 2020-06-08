import 'dart:ffi';
import 'dart:typed_data';

import 'package:ffi/ffi.dart';
import 'package:flutter/services.dart';


typedef oboe_stream_init = Pointer<Void> Function();
typedef OboeStreamInit = Pointer<Void> Function();

typedef oboe_stream_dispose = Void Function(Pointer<Void>);
typedef OboeStreamDispose = void Function(Pointer<Void>);

typedef oboe_stream_sample_rate = Int32 Function(Pointer<Void>);
typedef OboeStreamSampleRate = int Function(Pointer<Void>);

typedef oboe_stream_start_stop = Void Function(Pointer<Void>);
typedef OboeStreamStartStop = void Function(Pointer<Void>);

typedef oboe_stream_write = Void Function(Pointer<Void>, Pointer<Float>, Int32);
typedef OboeStreamWrite = void Function(Pointer<Void>, Pointer<Float>, int);

typedef oboe_load_file = Void Function();
typedef OboeLoadFile = void Function();


class FfiGoogleOboe {
  static const MethodChannel _channel =
      const MethodChannel('ffi_google_oboe');

  static Future<String> get platformVersion async {
    final String version = await _channel.invokeMethod('getPlatformVersion');
    return version;
  }

  static FfiGoogleOboe _instance;

  factory FfiGoogleOboe() {
    if (_instance == null) {
      _instance = FfiGoogleOboe._();
    }
    return _instance;
  }


  OboeStreamInit _streamInit;
  OboeStreamDispose _streamDispose;
  OboeStreamSampleRate _streamSampleRate;
  OboeStreamStartStop _streamStart;
  OboeStreamStartStop _streamStop;
  OboeStreamWrite _streamWrite;
  OboeLoadFile _loadFile;

  FfiGoogleOboe._() {
    final oboeLib = DynamicLibrary.open('libffi_google_oboe.so');

    _streamInit = oboeLib
        .lookup<NativeFunction<oboe_stream_init>>('stream_create')
        .asFunction();

    _streamDispose = oboeLib
        .lookup<NativeFunction<oboe_stream_dispose>>('stream_dispose')
        .asFunction();

    _streamSampleRate = oboeLib
        .lookup<NativeFunction<oboe_stream_sample_rate>>('stream_sample_rate')
        .asFunction();

    _streamStart = oboeLib
        .lookup<NativeFunction<oboe_stream_start_stop>>('stream_start')
        .asFunction();

    _streamStop = oboeLib
        .lookup<NativeFunction<oboe_stream_start_stop>>('stream_stop')
        .asFunction();

    _streamWrite = oboeLib
        .lookup<NativeFunction<oboe_stream_write>>('stream_write')
        .asFunction();

    _loadFile = oboeLib
        .lookup<NativeFunction<oboe_load_file>>('load_file')
        .asFunction();
  }

}


class OboeStream {
  Pointer<Void> _nativeInstance;

  OboeStream() {
    _nativeInstance = FfiGoogleOboe()._streamInit();
  }

  void dispose() {
    FfiGoogleOboe()._streamDispose(_nativeInstance);
  }

  int getSampleRate() {
    return FfiGoogleOboe()._streamSampleRate(_nativeInstance);
  }

  void start() {
    FfiGoogleOboe()._streamStart(_nativeInstance);
  }

  void stop() {
    FfiGoogleOboe()._streamStop(_nativeInstance);
  }

  void write(Float32List original) {
    var length = original.length;
    var copy = allocate<Float>(count: length)
        ..asTypedList(length).setAll(0, original);

    FfiGoogleOboe()._streamWrite(_nativeInstance, copy, length);
    free(copy);
  }

  void loadFile(String path) {
    
  }
}
