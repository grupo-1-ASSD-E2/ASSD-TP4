//
// Created by facun on 23/05/2020.
//

#ifndef ANDROID_OBOEFFISTREAM_H
#define ANDROID_OBOEFFISTREAM_H


#include <cstdint>
#include <string>
#include <variant>
#include <queue>
#include <vector>

#include <oboe/Oboe.h>
#include <audio/AAssetDataSource.h>
#include <audio/Player.h>
#include <shared/Mixer.h>

#include "DSPCallback.h"
#include "FunctionList.h"


class OboeFfiStream {
public:
    OboeFfiStream(int sr=48000, void * data=nullptr, size_t size=0, oboe::AudioFormat f=oboe::AudioFormat::Float);
    virtual ~OboeFfiStream() = default;

    int32_t getSampleRate();
    void close();
    void write(void * data, size_t size);

    void beginStreams();
    void startStreams();
    void stopStreams();
    bool loadAudioSource(uint8_t* data_buffer, size_t len);


    std::variant<FunctionList<int16_t *>, FunctionList<float *>> functionList{std::in_place_type<FunctionList<int16_t *>>};

private:
    void openOutStream();
    oboe::AudioStreamBuilder defaultBuilder();

    void createCallback();

    oboe::AudioFormat format;
    int sampleRate;
    std::queue<float> inQueue;

    std::unique_ptr<oboe::AudioStreamCallback> mCallback;
    oboe::ManagedStream outStream;
    Mixer mMixer;
    std::vector<std::unique_ptr<Player>> players;
};


#endif //ANDROID_OBOEFFISTREAM_H
