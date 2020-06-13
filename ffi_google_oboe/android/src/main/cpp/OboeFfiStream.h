//
// Created by facun on 23/05/2020.
//

#ifndef ANDROID_OBOEFFISTREAM_H
#define ANDROID_OBOEFFISTREAM_H


#include <oboe/Oboe.h>
#include <cstdint>
#include <variant>
#include <queue>

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
};


#endif //ANDROID_OBOEFFISTREAM_H
