//
// Created by facun on 3/07/2020.
//

#ifndef ANDROID_BUFFERMEDIADATASOURCE_H
#define ANDROID_BUFFERMEDIADATASOURCE_H

#include <media/NdkMediaDataSource.h>


class BufferMediaDataSource {

public:
    BufferMediaDataSource(AMediaDataSource* mDataSource, uint8_t* buffer, size_t len);
    AMediaDataSource* get();

    void configureCustomMediaSource();

    static ssize_t customMediaSourceReadAt(void *userdata, off64_t offset, void * buffer, size_t size);
    static ssize_t customMediaSourceGetSize(void *userdata);
    static void customMediaSourceClose(void *userdata);

    static uint8_t* dataBuffer;
    static size_t buffer_length;

private:
    AMediaDataSource* mediaDataSource;

};


#endif //ANDROID_BUFFERMEDIADATASOURCE_H
