//
// Created by facun on 23/05/2020.
//

#include "DSPAudioEngine.h"
#include <utils/logging.h>
#include <android/log.h>
#include <jni.h>
#include <android/asset_manager_jni.h>

#ifdef __cplusplus
#define EXTERNC extern "C"
#else
#define EXTERNC
#endif

EXTERNC void *engine_create(void) {
    AAssetManager *assetManager = AAssetManager_fromJava(env, jAssetManager);   // How do I get these?
    if (assetManager == nullptr) {
        LOGE("Could not obtain the AAssetManager");
        return nullptr;
    }   

    return new DSPAudioEngine(*assetManager);
}

EXTERNC void engine_dispose(void* ptr) {
    auto engine = static_cast<DSPAudioEngine*>(ptr);
    engine->close();
    delete engine;
}

EXTERNC int32_t engine_sample_rate(void* ptr) {
    return (static_cast<DSPAudioEngine*>(ptr))->getSampleRate();
}

EXTERNC void engine_start(void* ptr) {
    auto engine = static_cast<DSPAudioEngine*>(ptr);
    engine->startStreams();
}

EXTERNC void engine_stop(void* ptr) {
    auto engine = static_cast<DSPAudioEngine*>(ptr);
    engine->stopStreams();
}

EXTERNC void engine_write(void* ptr, void* data, int32_t size) {
    auto engine = static_cast<DSPAudioEngine*>(ptr);
    auto dataToWrite = static_cast<float*>(data);
    engine->write(dataToWrite, size);
}

EXTERNC int32_t engine_load_audio(void *ptr, char *path) {
    auto engine = static_cast<DSPAudioEngine*>(ptr);
    if (engine->loadAudioSource(path)) {
        return 1;
    }
    else {
        return 0;
    }

}