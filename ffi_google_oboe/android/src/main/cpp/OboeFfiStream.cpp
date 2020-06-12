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
    LOGE("STREAMS INITIALISED");
    LOGE(" ");
}

void OboeFfiStream::write(void * data, size_t size) {
    auto floatData = static_cast<float *>(data);
    inSource = std::vector<float>(floatData, floatData + size);
}

void OboeFfiStream::beginStreams() {
    functionList.emplace<FunctionList<float *>>().addEffect([](float*, float*){});
    createCallback();
    LOGE("CALLBACK CREATED SUCCESSFULLY");
    LOGE(" ");
    openOutStream();

    oboe::Result result = startStreams();
    if (result != oboe::Result::OK) stopStreams();
}

void OboeFfiStream::createCallback() {
    mCallback = std::make_unique<OboeFfiCallback<float>>(
            inSource,
            [&functionStack = this->functionList](float *beg, float *end) {
                std::get<FunctionList<float *>>(functionStack)(beg, end);
            },
            std::bind(&OboeFfiStream::beginStreams, this));
}


oboe::AudioStreamBuilder OboeFfiStream::defaultBuilder() {
    return *oboe::AudioStreamBuilder()
            .setPerformanceMode(oboe::PerformanceMode::LowLatency)
            ->setSharingMode(oboe::SharingMode::Shared);
}

void OboeFfiStream::openOutStream() {
    defaultBuilder().setCallback(mCallback.get())
            ->setSampleRate(sampleRate)
            ->setFormat(format)
            ->setChannelCount(2) // Stereo out
            ->openManagedStream(outStream);
}

oboe::Result OboeFfiStream::startStreams() {
    oboe::Result result = outStream->requestStart();
    int64_t timeoutNanos = 500 * 1000000; // arbitrary 1/2 second
    auto currentState = outStream->getState();
    auto nextState = oboe::StreamState::Unknown;
    while (result == oboe::Result::OK && currentState != oboe::StreamState::Started) {
        result = outStream->waitForStateChange(currentState, &nextState, timeoutNanos);
        currentState = nextState;
    }
    return result;
}

oboe::Result OboeFfiStream::stopStreams() {
    return outStream->requestStop();
}

int32_t OboeFfiStream::getSampleRate() {
    return sampleRate;
}

void OboeFfiStream::close() {
    outStream->close();
}
