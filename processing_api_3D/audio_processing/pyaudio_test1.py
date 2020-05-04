"""PyAudio Example: Play a wave file (callback version)."""

import pyaudio
import time
import sys
import pysofaconventions as sofa
import scipy.signal as ss
import numpy as np
import librosa

br1_data, br1_rate = librosa.load('C:/Users/facun/OneDrive/Desktop/ITBA/6C ASSD/ASSD-TP4/Resources/Audio files/Multitracks Bohemian Rhapsody/01 - Borap01.wav', sr=44.1e3, dtype=np.float32)
br2_data, br2_rate = librosa.load('C:/Users/facun/OneDrive/Desktop/ITBA/6C ASSD/ASSD-TP4/Resources/Audio files/Multitracks Bohemian Rhapsody/02 - Borap02.wav', sr=44.1e3, dtype=np.float32)
br3_data, br3_rate = librosa.load('C:/Users/facun/OneDrive/Desktop/ITBA/6C ASSD/ASSD-TP4/Resources/Audio files/Multitracks Bohemian Rhapsody/03 - Borap03.wav', sr=44.1e3, dtype=np.float32)
print(br3_data.dtype)
print(br3_data.size)
hrir = sofa.SOFAFile('C:/Users/facun/OneDrive/Desktop/ITBA/6C ASSD/ASSD-TP4/Resources/SOFA_Databases/HUTUBS/HRIRs/pp1_HRIRs_measured.sofa', 'r')
print(hrir.getDataIR()[202,0,:].dtype)

# instantiate PyAudio (1)
p = pyaudio.PyAudio()
count = 0
IR_left = hrir.getDataIR()[209,0,:].astype(np.float32)
IR_right = hrir.getDataIR()[209,1,:].astype(np.float32)

window = ss.hanning(2**10)
inv_window = 1 / window

# define callback (2)
def callback(in_data, frame_count, time_info, status):
    global count

    br1_frame = br1_data[frame_count*count : frame_count*(count+1)]
    br2_frame = br2_data[frame_count*count : frame_count*(count+1)]
    br3_frame = br3_data[frame_count*count : frame_count*(count+1)]

    br1_left = ss.oaconvolve(np.multiply(br1_frame, window), IR_left, mode='same')
    br1_right = ss.oaconvolve(np.multiply(br1_frame, window), IR_right, mode='same')
    br2_left = ss.oaconvolve(np.multiply(br2_frame, window), IR_left, mode='same')
    br2_right = ss.oaconvolve(np.multiply(br2_frame, window), IR_right, mode='same')
    br3_left = ss.oaconvolve(np.multiply(br3_frame, window), IR_left, mode='same')
    br3_right = ss.oaconvolve(np.multiply(br3_frame, window), IR_right, mode='same')

    min_len_left = min(br1_left.size, br2_left.size, br3_left.size)
    min_len_right = min(br1_right.size, br2_right.size, br3_right.size)

    br_left = 1/3 * br1_left[:min_len_left] + 1/3 * br2_left[:min_len_left] + 1/3 * br3_left[:min_len_left]
    br_right = 1/3 * br1_right[:min_len_right] + 1/3 * br2_right[:min_len_right] + 1/3 * br3_right[:min_len_right]

    ret_data = np.empty((br_left.size + br_right.size), dtype=br3_left.dtype)
    ret_data[1::2] = br_left
    ret_data[0::2] = br_right
    ret_data = ret_data.astype(np.float32).tostring()
    count += 1
    return (ret_data, pyaudio.paContinue)

# open stream using callback (3)
stream = p.open(format=pyaudio.paFloat32,
                channels=2,
                rate=int(br3_rate),
                output=True,
                stream_callback=callback,
                frames_per_buffer=2**10)

# start the stream (4)
stream.start_stream()

# wait for stream to finish (5)
while_count = 0
while stream.is_active():
    while_count += 1
    if while_count % 3 == 0:
        IR_left = hrir.getDataIR()[209,0,:].astype(np.float32)
        IR_right = hrir.getDataIR()[209,1,:].astype(np.float32)
    elif while_count % 3 == 1:
        IR_left = hrir.getDataIR()[202,0,:].astype(np.float32)
        IR_right = hrir.getDataIR()[202,1,:].astype(np.float32)
    elif while_count % 3 == 2:
        IR_left = hrir.getDataIR()[227,0,:].astype(np.float32)
        IR_right = hrir.getDataIR()[227,1,:].astype(np.float32)

    time.sleep(10)

# stop stream (6)
stream.stop_stream()
stream.close()

# close PyAudio (7)
p.terminate()