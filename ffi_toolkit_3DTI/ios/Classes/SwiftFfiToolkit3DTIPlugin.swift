import Flutter
import UIKit

public class SwiftFfiToolkit3DTIPlugin: NSObject, FlutterPlugin {
  public static func register(with registrar: FlutterPluginRegistrar) {
    let channel = FlutterMethodChannel(name: "ffi_toolkit_3DTI", binaryMessenger: registrar.messenger())
    let instance = SwiftFfiToolkit3DTIPlugin()
    registrar.addMethodCallDelegate(instance, channel: channel)
  }

  public func handle(_ call: FlutterMethodCall, result: @escaping FlutterResult) {
    result("iOS " + UIDevice.current.systemVersion)
  }
}
