//
// Created by facun on 10/06/2020.
//

#ifndef ANDROID_OBOEFFICALLBACK_H
#define ANDROID_OBOEFFICALLBACK_H

#include <oboe/Oboe.h>
#include <vector>



// This callback handles mono in, stereo out synchronized audio passthrough.
// It takes a function which operates on two pointers (beginning and end)
// of underlying data.

template<class numeric_type>
class OboeFfiCallback : public oboe::AudioStreamCallback {
public:

    OboeFfiCallback(std::vector<numeric_type>& inVect,
                    std::function<void(numeric_type *, numeric_type *)> fun,
                    std::function<void(void)> restartFunction) :
                    inSource(inVect), f(fun), restart(restartFunction) {}


    oboe::DataCallbackResult onAudioReady(oboe::AudioStream *outputStream, void *audioData, int32_t numFrames) override {
        auto *outputData = static_cast<numeric_type *>(audioData);
        auto outputChannelCount = outputStream->getChannelCount();

        // Silence first to simplify glitch detection
        std::fill(outputData, outputData + numFrames * outputChannelCount, 0);
        auto data_to_process = std::vector<numeric_type>(inSource.begin() + cycle_count * numFrames, inSource.begin() + (cycle_count + 1) * numFrames);

//        f(inputBuffer.get(), inputBuffer.get() + numFrames);
//        for (int i = 0; i < numFrames; i++) {
//            for (int j = 0; j < outputChannelCount; j++) {
//                *outputData++ = inputBuffer[i];
//            }
//        }
        return oboe::DataCallbackResult::Continue;
    }

    void onErrorAfterClose(oboe::AudioStream *, oboe::Result result) override {
        if (result == oboe::Result::ErrorDisconnected) {
            restart();
        }
    }


private:
    size_t cycle_count;
    std::vector<numeric_type>& inSource;
    std::function<void(numeric_type *, numeric_type *)> f;
    std::function<void(void)> restart;
};

#endif //ANDROID_OBOEFFICALLBACK_H
