//
// Created by facun on 23/05/2020.
//

#include "OboeFfiStream.h"
#include <utils/logging.h>

// The Sample Rate for effects
static int SAMPLE_RATE = 48000;

OboeFfiStream::OboeFfiStream() {
    beginStreams();
}

void OboeFfiStream::beginStreams() {
    // This ordering is extremely important
    openInStream();
    if (inStream->getFormat() == oboe::AudioFormat::Float) {
        functionList.emplace<FunctionList<float *>>().addEffect([](float*, float*){});
        createCallback<float_t>();
    } else if (inStream->getFormat() == oboe::AudioFormat::I16) {
        createCallback<int16_t>();
    } else {
        stopStreams();
    }
    SAMPLE_RATE = inStream->getSampleRate();
    openOutStream();

    oboe::Result result = startStreams();
    if (result != oboe::Result::OK) stopStreams();
}

template<class numeric>
void OboeFfiStream::createCallback() {
    mCallback = std::make_unique<OboeFfiCallback<numeric>>(
            *inStream, [&functionStack = this->functionList](numeric *beg, numeric *end) {
                std::get<FunctionList<numeric *>>(functionStack)(beg, end);
            },
            inStream->getBufferCapacityInFrames(),
            std::bind(&OboeFfiStream::beginStreams, this));
}


oboe::AudioStreamBuilder OboeFfiStream::defaultBuilder() {
    return *oboe::AudioStreamBuilder()
            .setPerformanceMode(oboe::PerformanceMode::LowLatency)
            ->setSharingMode(oboe::SharingMode::Shared);
}

void OboeFfiStream::openInStream() {
    defaultBuilder().setDirection(oboe::Direction::Input)
            ->setFormat(oboe::AudioFormat::Float) // For now
            ->setChannelCount(1) // Mono in for effects processing
            ->openManagedStream(inStream);
}

void OboeFfiStream::openOutStream() {
    defaultBuilder().setCallback(mCallback.get())
            ->setSampleRate(inStream->getSampleRate())
            ->setFormat(inStream->getFormat())
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
    if (result != oboe::Result::OK) return result;
    return inStream->requestStart();
}

oboe::Result OboeFfiStream::stopStreams() {
    oboe::Result outputResult = inStream->requestStop();
    oboe::Result inputResult = outStream->requestStop();
    if (outputResult != oboe::Result::OK) return outputResult;
    return inputResult;
}

int32_t OboeFfiStream::getSampleRate() {
    return inStream->getSampleRate();
}

void OboeFfiStream::close() {
    inStream->close();
    outStream->close();
}

void OboeFfiStream::write(float *data, int32_t size) {
    inStream->write(data, size, 1000000);
}
