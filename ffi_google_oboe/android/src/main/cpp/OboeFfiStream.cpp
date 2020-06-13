//
// Created by facun on 23/05/2020.
//

#include "OboeFfiStream.h"
#include <utils/logging.h>


OboeFfiStream::OboeFfiStream(int sr, void * data, size_t size, oboe::AudioFormat f) {
    format = oboe::AudioFormat::Float;      // In the future could be changed to accept argument f.
    sampleRate = sr;
    write(data, size);
    LOGE("INPUT DATA WRITTEN");
    LOGE(" ");

    beginStreams();
}

void OboeFfiStream::write(void * data, size_t size) {
    if (data == nullptr) {
        inQueue.push(0);
    }
    else {
        auto floatData = static_cast<float *>(data);
        for (size_t i = 0; i < size; ++i) {
            inQueue.push(*floatData);
            floatData++;
        }
    }
    createCallback();
}

void OboeFfiStream::beginStreams() {
    functionList.emplace<FunctionList<float *>>().addEffect([](float*, float*){});
    createCallback();
    LOGE("CALLBACK CREATED SUCCESSFULLY");
    LOGE(" ");
    openOutStream();
}

void OboeFfiStream::createCallback() {
    mCallback = std::make_unique<DSPCallback>(
            inQueue,
            [&functionStack = this->functionList](float *beg, float *end) {
                std::get<FunctionList<float *>>(functionStack)(beg, end);
            },
            std::bind(&OboeFfiStream::beginStreams, this));
}


oboe::AudioStreamBuilder OboeFfiStream::defaultBuilder() {
    return *oboe::AudioStreamBuilder()
            .setPerformanceMode(oboe::PerformanceMode::LowLatency)
            ->setSharingMode(oboe::SharingMode::Shared)
            ->setSampleRate(sampleRate)
            ->setFormat(format);
}

void OboeFfiStream::openOutStream() {
    oboe::AudioStreamBuilder builder = defaultBuilder();
    builder.setChannelCount(2); // Stereo out
    builder.setCallback(mCallback.get());
    LOGE("BUILDER CONFIGURATIONS OK");
    LOGE(" ");

    builder.openManagedStream(outStream);
}

void OboeFfiStream::startStreams() {
    oboe::Result result = outStream->requestStart();
    int64_t timeoutNanos = 500 * 1000000; // arbitrary 1/2 second
    auto currentState = outStream->getState();
    auto nextState = oboe::StreamState::Unknown;
    while (result == oboe::Result::OK && currentState != oboe::StreamState::Started) {
        result = outStream->waitForStateChange(currentState, &nextState, timeoutNanos);
        currentState = nextState;
    }

    if (result != oboe::Result::OK) {
        stopStreams();
    }
    else {
        LOGE("STREAM STARTED SUCCESSFULLY");
        LOGE(" ");
    }
}

void OboeFfiStream::stopStreams() {
    oboe::Result result = outStream->requestStop();

    if (result != oboe::Result::OK) {
        stopStreams();
    }
    else {
        LOGE("STREAM STOPPED SUCCESSFULLY");
        LOGE(" ");
    }
}

int32_t OboeFfiStream::getSampleRate() {
    return sampleRate;
}

void OboeFfiStream::close() {
    outStream->close();
}
