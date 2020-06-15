import 'dart:ffi';
import 'dart:typed_data';

import 'package:ffi/ffi.dart';
import 'package:flutter/services.dart';


typedef oboe_engine_init = Pointer<Void> Function();
typedef OboeEngineInit = Pointer<Void> Function();

typedef oboe_engine_dispose = Void Function(Pointer<Void>);
typedef OboeEngineDispose = void Function(Pointer<Void>);

typedef oboe_engine_sample_rate = Int32 Function(Pointer<Void>);
typedef OboeEngineSampleRate = int Function(Pointer<Void>);

typedef oboe_engine_start_stop = Void Function(Pointer<Void>);
typedef OboeEngineStartStop = void Function(Pointer<Void>);

typedef oboe_engine_write = Void Function(Pointer<Void>, Pointer<Float>, Int32);
typedef OboeEngineWrite = void Function(Pointer<Void>, Pointer<Float>, int);

typedef oboe_engine_load_file = Int32 Function(Pointer<Void>, Pointer<Utf8>);
typedef OboeEngineLoadFile = int Function(Pointer<Void>, Pointer<Utf8>);


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


  OboeEngineInit _engineInit;
  OboeEngineDispose _engineDispose;
  OboeEngineSampleRate _engineSampleRate;
  OboeEngineStartStop _engineStart;
  OboeEngineStartStop _engineStop;
  OboeEngineWrite _engineWrite;
  OboeEngineLoadFile _engineLoadFile;

  FfiGoogleOboe._() {
    final oboeLib = DynamicLibrary.open('libffi_google_oboe.so');

    _engineInit = oboeLib
        .lookup<NativeFunction<oboe_engine_init>>('engine_create')
        .asFunction();

    _engineDispose = oboeLib
        .lookup<NativeFunction<oboe_engine_dispose>>('engine_dispose')
        .asFunction();

    _engineSampleRate = oboeLib
        .lookup<NativeFunction<oboe_engine_sample_rate>>('engine_sample_rate')
        .asFunction();

    _engineStart = oboeLib
        .lookup<NativeFunction<oboe_engine_start_stop>>('engine_start')
        .asFunction();

    _engineStop = oboeLib
        .lookup<NativeFunction<oboe_engine_start_stop>>('engine_stop')
        .asFunction();

    _engineWrite = oboeLib
        .lookup<NativeFunction<oboe_engine_write>>('engine_write')
        .asFunction();

    _engineLoadFile = oboeLib
        .lookup<NativeFunction<oboe_engine_load_file>>('engine_load_audio')
        .asFunction();
  }

}


class OboeEngine {
  Pointer<Void> _nativeInstance;

  OboeEngine() {
    _nativeInstance = FfiGoogleOboe()._engineInit();
  }

  void dispose() {
    FfiGoogleOboe()._engineDispose(_nativeInstance);
  }

  int getSampleRate() {
    return FfiGoogleOboe()._engineSampleRate(_nativeInstance);
  }

  void start() {
    FfiGoogleOboe()._engineStart(_nativeInstance);
  }

  void stop() {
    FfiGoogleOboe()._engineStop(_nativeInstance);
  }

  void write(Float32List original) {
    var length = original.length;
    var copy = allocate<Float>(count: length)
        ..asTypedList(length).setAll(0, original);

    FfiGoogleOboe()._engineWrite(_nativeInstance, copy, length);
    free(copy);
  }
}
