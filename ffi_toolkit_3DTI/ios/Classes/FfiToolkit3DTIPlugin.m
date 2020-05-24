#import "FfiToolkit3DTIPlugin.h"
#if __has_include(<ffi_toolkit_3DTI/ffi_toolkit_3DTI-Swift.h>)
#import <ffi_toolkit_3DTI/ffi_toolkit_3DTI-Swift.h>
#else
// Support project import fallback if the generated compatibility header
// is not copied when this plugin is created as a library.
// https://forums.swift.org/t/swift-static-libraries-dont-copy-generated-objective-c-header/19816
#import "ffi_toolkit_3DTI-Swift.h"
#endif

@implementation FfiToolkit3DTIPlugin
+ (void)registerWithRegistrar:(NSObject<FlutterPluginRegistrar>*)registrar {
  [SwiftFfiToolkit3DTIPlugin registerWithRegistrar:registrar];
}
@end
