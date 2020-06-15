//
// Created by facun on 23/05/2020.
//

#include "DSPAudioEngine.h"
#include <utils/logging.h>
#include <android/log.h>

#ifdef __cplusplus
#define EXTERNC extern "C"
#else
#define EXTERNC
#endif

EXTERNC void* stream_create() {
    LOGE("CREATING STREAM");
    LOGE(" ");
    return new DSPAudioEngine();
}

EXTERNC void stream_dispose(void* ptr) {
    auto stream = static_cast<DSPAudioEngine*>(ptr);
    stream->close();
    delete stream;
}

EXTERNC int32_t stream_sample_rate(void* ptr) {
    return (static_cast<DSPAudioEngine*>(ptr))->getSampleRate();
}

EXTERNC void stream_start(void* ptr) {
    auto stream = static_cast<DSPAudioEngine*>(ptr);
    stream->startStreams();
}

EXTERNC void stream_stop(void* ptr) {
    auto stream = static_cast<DSPAudioEngine*>(ptr);
    stream->stopStreams();
}

EXTERNC void stream_write(void* ptr, void* data, int32_t size) {
    auto stream = static_cast<DSPAudioEngine*>(ptr);
    auto dataToWrite = static_cast<float*>(data);
    stream->write(dataToWrite, size);
}