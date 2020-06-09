//
// Created by facun on 23/05/2020.
//

#include "OboeFfiStream.h"
#include "utils/logging.h"
#include <android/asset_manager_jni.h>

#ifdef __cplusplus
#define EXTERNC extern "C"
#else
#define EXTERNC
#endif

EXTERNC void* stream_create() {
    AAssetManager* assetManager = AAssetManager_fromJava(env, jAssetManager);
    if (assetManager == nullptr) {
        LOGE("Could not obtain the AAssetManager");
        return nullptr;
    }

    return new OboeFfiStream(*assetManager);
}

EXTERNC void stream_dispose(void* ptr) {
    auto stream = static_cast<OboeFfiStream*>(ptr);
    stream->close();
    delete stream;
}

EXTERNC int32_t stream_sample_rate(void* ptr) {
    return (static_cast<OboeFfiStream*>(ptr))->getSampleRate();
}

EXTERNC void stream_start(void* ptr) {
    auto stream = static_cast<OboeFfiStream*>(ptr);
    stream->start();
}

EXTERNC void stream_stop(void* ptr) {
    auto stream = static_cast<OboeFfiStream*>(ptr);
    stream->stop();
}

EXTERNC void stream_write(void* ptr, void* data, int32_t size) {
    auto stream = static_cast<OboeFfiStream*>(ptr);
    auto dataToWrite = static_cast<float*>(data);
    stream->write(dataToWrite, size);
}

EXTERNC void load_file(void* ptr) {

}