//
// Created by facun on 23/05/2020.
//

#ifndef ANDROID_DSPAUDIOENGINE_H
#define ANDROID_DSPAUDIOENGINE_H


#include <cstdint>
#include <string>
#include <variant>
#include <queue>
#include <vector>

#include <oboe/Oboe.h>
#include <audio/AAssetDataSource.h>
#include <audio/Player.h>
#include <shared/Mixer.h>

#include "DSPCallback.h"
#include "FunctionList.h"


class DSPAudioEngine {
public:
    DSPAudioEngine(AAssetManager& aManager, int sr=48000, void * data=nullptr, size_t size=0, oboe::AudioFormat f=oboe::AudioFormat::Float);
    virtual ~DSPAudioEngine() = default;

    int32_t getSampleRate();
    void close();
    void write(void * data, size_t size);

    void beginStreams();
    void startStreams();
    void stopStreams();
    bool loadAudioSource(std::string path);


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
    Mixer mMixer;
    std::vector<Player> players;

    AAssetManager &mAssetManager;
};


#endif //ANDROID_DSPAUDIOENGINE_H
