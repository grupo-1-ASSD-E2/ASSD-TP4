//
// Created by facun on 23/05/2020.
//

#ifndef ANDROID_OBOEFFISTREAM_H
#define ANDROID_OBOEFFISTREAM_H


#include <oboe/Oboe.h>
#include <cstdint>
#include <cstring>
#include <array>
#include <algorithm>
#include <variant>

#include "OboeFfiCallback.h"
#include "FunctionList.h"


class OboeFfiStream {
public:
    OboeFfiStream();
    virtual ~OboeFfiStream() = default;

    int32_t getSampleRate();
    void close();
    void start();
    void stop();
    void write(float* data, int32_t size);

    void beginStreams();
    oboe::Result startStreams();
    oboe::Result stopStreams();


    std::variant<FunctionList<int16_t *>, FunctionList<float *>> functionList{std::in_place_type<FunctionList<int16_t *>>};

private:

    void openInStream();
    void openOutStream();
    static oboe::AudioStreamBuilder defaultBuilder();

    template<class numeric>
    void createCallback();

    oboe::ManagedStream inStream;
    std::unique_ptr<oboe::AudioStreamCallback> mCallback;
    oboe::ManagedStream outStream;

    oboe::ManagedStream managedStream;
};


#endif //ANDROID_OBOEFFISTREAM_H
