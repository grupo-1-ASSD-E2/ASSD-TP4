//
// Created by facun on 23/05/2020.
//

#include <oboe/AudioStreamBuilder.h>
#include "OboeFfiStream.h"

OboeFfiStream::OboeFfiStream() {
    oboe::AudioStreamBuilder builder;
    builder.setFormat(oboe::AudioFormat::Float)
        ->setChannelCount(oboe::ChannelCount::Mono);
    builder.setSampleRate(48000);

    oboe::Result result = builder.openManagedStream(managedStream);
}

int32_t OboeFfiStream::getSampleRate() {
    return managedStream->getSampleRate();
}

void OboeFfiStream::close() {
    managedStream->close();
}

void OboeFfiStream::start() {
    managedStream->requestStart();
}

void OboeFfiStream::stop() {
    managedStream->requestStop();
}

void OboeFfiStream::write(float *data, int32_t size) {
    managedStream->write(data, size, 1000000);
}
