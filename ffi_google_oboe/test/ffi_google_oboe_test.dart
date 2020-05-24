import 'package:flutter/services.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:ffi_google_oboe/ffi_google_oboe.dart';

void main() {
  const MethodChannel channel = MethodChannel('ffi_google_oboe');

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
    expect(await FfiGoogleOboe.platformVersion, '42');
  });
}
