//
// Created by facun on 12/06/2020.
//

#ifndef ANDROID_DSPCALLBACK_H
#define ANDROID_DSPCALLBACK_H

#include <oboe/Oboe.h>
#include <queue>
#include <utils/logging.h>


class DSPCallback : public oboe::AudioStreamCallback {
public:
    DSPCallback(std::queue<float>& inQ, std::function<void(float *, float *)> fun, std::function<void(void)> restartFunction);
    oboe::DataCallbackResult onAudioReady(oboe::AudioStream *outputStream, void *audioData, int32_t numFrames) override;
    void onErrorAfterClose(oboe::AudioStream *, oboe::Result result) override;


private:
    size_t cycle_count=0;
    std::queue<float>& inQueue;
    std::function<void(float *, float *)> f;
    std::function<void(void)> restart;
};


#endif //ANDROID_DSPCALLBACK_H
