//
// Created by facun on 23/05/2020.
//

#ifndef ANDROID_OBOEFFISTREAM_H
#define ANDROID_OBOEFFISTREAM_H

#include "oboe/Oboe.h"
#include <cstdint>
#include <cstring>

class OboeFfiStream {
public:
    OboeFfiStream();

    int32_t getSampleRate();
    void close();
    void start();
    void stop();
    void write(float* data, int32_t size);
    bool loadAudioSource(std::string path);


private:
    oboe::ManagedStream managedStream;
};


#endif //ANDROID_OBOEFFISTREAM_H
