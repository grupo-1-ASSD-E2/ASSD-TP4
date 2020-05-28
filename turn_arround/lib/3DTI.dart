import 'dart:ffi'; // For FFI
import 'dart:io';

typedef stringFun = IntPtr Function();

final DynamicLibrary nativeLib = Platform.isAndroid
    ? DynamicLibrary.open("lib_3DTIMobile.so")
    : DynamicLibrary.process();

final Pointer<NativeFunction<stringFun>> natFun = 
  nativeLib
    .lookup<NativeFunction<stringFun>>("message_simple");

final stringFun messageSimple = natFun.asFunction();
  // nativeLib
  //   .lookup<NativeFunction<String Function(void)>>("message_simple")
  //   .asFunction();
