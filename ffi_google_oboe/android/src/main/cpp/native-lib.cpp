//
// Created by facun on 15/06/2020.
//

#include <jni.h>
#include <memory>

#include <android/asset_manager_jni.h>

#include <utils/logging.h>
#include "DSPAudioEngine.h"


extern "C" {

std::unique_ptr<DSPAudioEngine> engine;

JNIEXPORT void JNICALL
Java_com_google_oboe_sample_rhythmgame_MainActivity_native_1engineCreate(JNIEnv *env, jobject instance, jobject jAssetManager) {

    AAssetManager *assetManager = AAssetManager_fromJava(env, jAssetManager);
    if (assetManager == nullptr) {
        LOGE("Could not obtain the AAssetManager");
        return;
    }

    engine = std::make_unique<DSPAudioEngine>(*assetManager);
}

JNIEXPORT void JNICALL
Java_com_google_oboe_sample_rhythmgame_MainActivity_native_1engineDispose(JNIEnv *env, void *ptr) {

}

JNIEXPORT int32_t JNICALL
Java_com_google_oboe_sample_rhythmgame_MainActivity_native_1engineSampleRate(JNIEnv *env, void *ptr) {
    return (static_cast<DSPAudioEngine*>(ptr))->getSampleRate();
}



}