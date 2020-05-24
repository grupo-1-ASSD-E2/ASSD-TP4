import 'package:flutter/services.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:ffi_toolkit_3DTI/ffi_toolkit_3DTI.dart';

void main() {
  const MethodChannel channel = MethodChannel('ffi_toolkit_3DTI');

  TestWidgetsFlutterBinding.ensureInitialized();

  setUp(() {
    channel.setMockMethodCallHandler((MethodCall methodCall) async {
      return '42';
    });
  });

  tearDown(() {
    channel.setMockMethodCallHandler(null);
  });

  test('getPlatformVersion', () async {
    expect(await FfiToolkit3DTI.platformVersion, '42');
  });
}
