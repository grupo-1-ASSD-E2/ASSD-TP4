//
// Created by facun on 23/05/2020.
//

#include "OboeFfiStream.h"
#include <utils/logging.h>
#include <android/log.h>
#include <android/asset_manager_jni.h>
#include <jni.h>
//#include <SDL/include/SDL.h>

#ifdef __cplusplus
#define EXTERNC extern "C"
#else
#define EXTERNC
#endif

EXTERNC void* stream_create() {
    LOGE("CREATING STREAM");
    LOGE(" ");

//    auto env = (JNIEnv *)SDL_AndroidGetJNIEnv();
//    auto activity = (jobject)SDL_AndroidGetActivity();

    JNIEnv * g_env;
    // double check it's all ok
    int getEnvStat = g_vm->GetEnv((void **)&g_env, JNI_VERSION_1_6);
    if (getEnvStat == JNI_EDETACHED) {
        std::cout << "GetEnv: not attached" << std::endl;
        if (g_vm->AttachCurrentThread((void **) &g_env, NULL) != 0) {
            std::cout << "Failed to attach" << std::endl;
        }
    } else if (getEnvStat == JNI_OK) {
        //
    } else if (getEnvStat == JNI_EVERSION) {
        std::cout << "GetEnv: version not supported" << std::endl;
    }

    if (env == 0) {
        LOGE("Could not obtain JNIEnv.");
        LOGE(" ");
        return nullptr;
    }
    else if (activity == NULL) {
        LOGE("Could not obtain jobject activity.");
        LOGE(" ");
        return nullptr;
    }

    jclass activityClass = env->GetObjectClass(activity);

    jmethodID activityClassGetAssets = env->GetMethodID(activityClass, "getAssets", "()Landroid/content/res/AssetManager;");
    jobject jAssetManager = env->CallObjectMethod(activity, activityClassGetAssets); // activity.getAssets();

    AAssetManager *assetManager = AAssetManager_fromJava(env, jAssetManager);
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
    stream->startStreams();
}

EXTERNC void stream_stop(void* ptr) {
    auto stream = static_cast<OboeFfiStream*>(ptr);
    stream->stopStreams();
}

EXTERNC void stream_write(void* ptr, void* data, int32_t size) {
    auto stream = static_cast<OboeFfiStream*>(ptr);
    auto dataToWrite = static_cast<float*>(data);
    stream->write(dataToWrite, size);
}