//
// Created by facun on 10/06/2020.
//

#ifndef ANDROID_OBOEFFICALLBACK_H
#define ANDROID_OBOEFFICALLBACK_H

#include <oboe/Oboe.h>



// This callback handles mono in, stereo out synchronized audio passthrough.
// It takes a function which operates on two pointers (beginning and end)
// of underlying data.

template<class numeric_type>
class OboeFfiCallback : public oboe::AudioStreamCallback {
public:

    OboeFfiCallback(oboe::AudioStream &inStream,
                    std::function<void(numeric_type *, numeric_type *)> fun,
                    size_t buffer_size, std::function<void(void)> restartFunction) :
            kBufferSize(buffer_size), inRef(inStream), f(fun), restart(restartFunction) {}


    oboe::DataCallbackResult onAudioReady(oboe::AudioStream *outputStream, void *audioData, int32_t numFrames) override {
        auto *outputData = static_cast<numeric_type *>(audioData);
        auto outputChannelCount = outputStream->getChannelCount();

        // Silence first to simplify glitch detection
        std::fill(outputData, outputData + numFrames * outputChannelCount, 0);
        oboe::ResultWithValue<int32_t> result = inRef.read(inputBuffer.get(), numFrames, 0);
        int32_t framesRead = result.value();
        if (!result) {
            inRef.requestStop();
            return oboe::DataCallbackResult::Stop;
        }
        if (mSpinUpCallbacks > 0 && framesRead > 0) {
            mSpinUpCallbacks--;
            return oboe::DataCallbackResult::Continue;
        }
        f(inputBuffer.get(), inputBuffer.get() + framesRead);
        for (int i = 0; i < framesRead; i++) {
            for (size_t j = 0; j < outputChannelCount; j++) {
                *outputData++ = inputBuffer[i];
            }
        }
        return oboe::DataCallbackResult::Continue;
    }

    void onErrorAfterClose(oboe::AudioStream *, oboe::Result result) override {
        inRef.close();
        if (result == oboe::Result::ErrorDisconnected) {
            restart();
        }
    }


private:
    int mSpinUpCallbacks = 10; // We will let the streams sync for the first few valid frames
    const size_t kBufferSize;
    oboe::AudioStream &inRef;
    std::function<void(numeric_type *, numeric_type *)> f;
    std::function<void(void)> restart;
    std::unique_ptr<numeric_type[]> inputBuffer = std::make_unique<numeric_type[]>(kBufferSize);
};

#endif //ANDROID_OBOEFFICALLBACK_H
