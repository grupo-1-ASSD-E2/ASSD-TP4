//
// Created by facun on 3/07/2020.
//

#include <functional>
#include "BufferMediaDataSource.h"

uint8_t* BufferMediaDataSource::dataBuffer = nullptr;
size_t BufferMediaDataSource::buffer_length = 0;

BufferMediaDataSource::BufferMediaDataSource(AMediaDataSource *mDataSource, uint8_t* b, size_t len) : mediaDataSource(mDataSource){
    dataBuffer = b;
    buffer_length = len;
    configureCustomMediaSource();
}

AMediaDataSource *BufferMediaDataSource::get() {
    return mediaDataSource;
}

void BufferMediaDataSource::configureCustomMediaSource() {
    AMediaDataSource_setReadAt(mediaDataSource, customMediaSourceReadAt);
    AMediaDataSource_setGetSize(mediaDataSource, customMediaSourceGetSize);
    AMediaDataSource_setClose(mediaDataSource, customMediaSourceClose);
}

ssize_t BufferMediaDataSource::customMediaSourceReadAt(void *userdata, off64_t offset, void *buffer, size_t size) {
    auto bufferRead = static_cast<uint8_t *>(buffer);

    for (int i = 0; i < size; ++i) {
        if (offset + i < buffer_length) {
            bufferRead[i] = dataBuffer[offset + i];
        }
        else {
            return -1;
        }
    }

    return size;
}

ssize_t BufferMediaDataSource::customMediaSourceGetSize(void *userdata) {
    return buffer_length;
}

void BufferMediaDataSource::customMediaSourceClose(void *userdata) {

}
