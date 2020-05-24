#import "FfiGoogleOboePlugin.h"
#if __has_include(<ffi_google_oboe/ffi_google_oboe-Swift.h>)
#import <ffi_google_oboe/ffi_google_oboe-Swift.h>
#else
// Support project import fallback if the generated compatibility header
// is not copied when this plugin is created as a library.
// https://forums.swift.org/t/swift-static-libraries-dont-copy-generated-objective-c-header/19816
#import "ffi_google_oboe-Swift.h"
#endif

@implementation FfiGoogleOboePlugin
+ (void)registerWithRegistrar:(NSObject<FlutterPluginRegistrar>*)registrar {
  [SwiftFfiGoogleOboePlugin registerWithRegistrar:registrar];
}
@end
