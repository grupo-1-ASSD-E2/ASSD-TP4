//
// Created by facun on 23/05/2020.
//

#include <oboe/AudioStreamBuilder.h>
//#include "audio/AAssetDataSource.h"
#include "OboeFfiStream.h"
#include "utils/logging.h"

OboeFfiStream::OboeFfiStream() {
    oboe::AudioStreamBuilder builder;
    builder.setFormat(oboe::AudioFormat::Float)
        ->setChannelCount(oboe::ChannelCount::Mono);
    builder.setSampleRate(44100);

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
