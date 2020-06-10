//
// Created by facun on 23/05/2020.
//

#include "OboeFfiStream.h"
#include "utils/logging.h"

OboeFfiStream::OboeFfiStream() {
    createInputStream();
    createOutputStream();
}

void OboeFfiStream::createInputStream() {
    oboe::AudioStreamBuilder builder = getBuilder();

    builder.setDirection(oboe::Direction::Input);
    builder.openManagedStream(inputStream);

}

void OboeFfiStream::createOutputStream() {
    oboe::AudioStreamBuilder builder = getBuilder();

    builder.setDirection(oboe::Direction::Output);
    builder.openManagedStream(outputStream);

}

oboe::AudioStreamBuilder OboeFfiStream::getBuilder() {
    oboe::AudioStreamBuilder builder;
    builder.setPerformanceMode(oboe::PerformanceMode::LowLatency);
    builder.setSharingMode(oboe::SharingMode::Exclusive);

    builder.setFormat(oboe::AudioFormat::Float);
    builder.setSampleRate(48000);
    builder.setChannelCount(oboe::ChannelCount::Mono);

    builder.setSampleRateConversionQuality(oboe::SampleRateConversionQuality::Medium);
    builder.setChannelConversionAllowed(true);
    builder.setFormatConversionAllowed(true);

    return builder;
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

bool OboeFfiStream::loadAudioSource(std::string path) {
//    std::shared_ptr<AAssetDataSource> mClapSource {
//            AAssetDataSource::newFromCompressedAsset(mAssetManager, "CLAP.mp3")
//    };
//    if (mClapSource == nullptr) {
//        LOGE("Could not load source data for clap sound");
//        return false;
//    }

    return true;
}
