//
// Created by facun on 10/06/2020.
//

#ifndef ANDROID_OBOEFFICALLBACK_H
#define ANDROID_OBOEFFICALLBACK_H

#include <oboe/Oboe.h>
#include <queue>
#include <utils/logging.h>



// This callback handles mono in, stereo out synchronized audio passthrough.
// It takes a function which operates on two pointers (beginning and end)
// of underlying data.

class OboeFfiCallback : public oboe::AudioStreamCallback {
public:

    OboeFfiCallback(std::queue<float>& inQ,
                    std::function<void(float *, float *)> fun,
                    std::function<void(void)> restartFunction) :
                    inQueue(inQ), f(fun), restart(restartFunction) {}


    oboe::DataCallbackResult onAudioReady(oboe::AudioStream *outputStream, void *audioData, int32_t numFrames) override {
        LOGE("CALLBACK CALLED");
        LOGE("numFrames = %d", numFrames);
        LOGE("Frames left in inQueue = %d", inQueue.size());
        auto *outputData = static_cast<float *>(audioData);
        auto outputChannelCount = outputStream->getChannelCount();

        // Silence first to simplify glitch detection
        std::fill(outputData, outputData + numFrames * outputChannelCount, 0);

        if (inQueue.size() > 0){
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

    void onErrorAfterClose(oboe::AudioStream *, oboe::Result result) override {
        if (result == oboe::Result::ErrorDisconnected) {
            restart();
        }
    }


private:
    size_t cycle_count;
    std::queue<float>& inQueue;
    std::function<void(float *, float *)> f;
    std::function<void(void)> restart;
};

#endif //ANDROID_OBOEFFICALLBACK_H
