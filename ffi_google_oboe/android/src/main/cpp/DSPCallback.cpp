//
// Created by facun on 12/06/2020.
//

#include "DSPCallback.h"

#include <utility>

DSPCallback::DSPCallback(std::queue<float> &inQ, std::function<void(float *, float *)> fun, std::function<void(void)> restartFunction)
: inQueue(inQ), f(std::move(fun)), restart(std::move(restartFunction)) {}

oboe::DataCallbackResult DSPCallback::onAudioReady(oboe::AudioStream *outputStream, void *audioData, int32_t numFrames) {
    LOGE("CALLBACK CALLED");
    LOGE("numFrames = %d", numFrames);
    LOGE("Frames left in inQueue = %d", inQueue.size());
    auto *outputData = static_cast<float *>(audioData);
    auto outputChannelCount = outputStream->getChannelCount();

    // Silence first to simplify glitch detection
    std::fill(outputData, outputData + numFrames * outputChannelCount, 0);

    if (!inQueue.empty()){
        LOGE("PROCESSING DATA");
        LOGE(" ");
        // Processing (for now it's just pass-through)
        for (int i = 0; i < numFrames; i++) {
            float temp_sound = inQueue.front();
            inQueue.pop();
            for (int j = 0; j < outputChannelCount; j++) {
                *outputData++ = temp_sound;
            }
        }
    }
    else {
        LOGE("NO DATA TO PROCESS");
        LOGE(" ");
    }
    return oboe::DataCallbackResult::Continue;
}

void DSPCallback::onErrorAfterClose(oboe::AudioStream *, oboe::Result result) {
    if (result == oboe::Result::ErrorDisconnected) {
        restart();
    }
}


