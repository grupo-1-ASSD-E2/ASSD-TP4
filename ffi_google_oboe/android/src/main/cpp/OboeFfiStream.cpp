//
// Created by facun on 23/05/2020.
//

#include "OboeFfiStream.h"
#include <utils/logging.h>


OboeFfiStream::OboeFfiStream(AAssetManager &assetManager, int sr, void * data, size_t size, oboe::AudioFormat f) : sampleRate(sr), mAssetManager(assetManager) {
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
            ->setFormat(format)
            ->setFramesPerCallback(512);
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

bool OboeFfiStream::loadAudioSource(std::string path) {

    // Set the properties of our audio source(s) to match that of our audio stream
    AudioProperties targetProperties {outStream->getChannelCount(),outStream->getSampleRate()};

    // Create a data source and player for our backing track
    std::shared_ptr<AAssetDataSource> backingTrackSource {
            AAssetDataSource::newFromCompressedAsset(mAssetManager, path.c_str(), &targetProperties)
    };
    if (backingTrackSource == nullptr){
        LOGE("Could not load source data for backing track");
        return false;
    }
    players.emplace_back(std::make_unique<Player>(backingTrackSource));

    // Adding player to a mixer
    mMixer.addTrack(players.back().get());

    return true;
}
