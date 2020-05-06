"""PyAudio Example: Play a wave file (callback version)."""

import pyaudio
import time
import sys
import pysofaconventions as sofa
import scipy.signal as ss
import numpy as np
import librosa
from midi2audio import FluidSynth

fs = FluidSynth()
fs.midi_to_audio('Sweet Child O Mine.mid', "hola.wav")

scof_data, scof_rate = librosa.load('C:/Users/facun/OneDrive/Desktop/ITBA/6C ASSD/ASSD-TP4/Resources/Audio files/MIDI files/Guns n Roses - Sweet Child O Mine.wav', sr=44.1e3, dtype=np.float32)
print(scof_data.dtype)
print(scof_data.size)
hrir = sofa.SOFAFile('C:/Users/facun/OneDrive/Desktop/ITBA/6C ASSD/ASSD-TP4/Resources/SOFA_Databases/HUTUBS/HRIRs/pp1_HRIRs_measured.sofa', 'r')
print(hrir.getDataIR()[202,0,:].dtype)

# instantiate PyAudio (1)
p = pyaudio.PyAudio()
count = 0
IR_left = hrir.getDataIR()[209,0,:].astype(np.float32)
IR_right = hrir.getDataIR()[209,1,:].astype(np.float32)

add_leftover = np.zeros((2, 2**10 + 255), dtype=np.float32)

# define callback (2)
def callback(in_data, frame_count, time_info, status):
    global count

    scof_frame = scof_data[frame_count*count : frame_count*(count+1)]

    scof_left = ss.oaconvolve(scof_frame, IR_left, mode='full') + add_leftover[0]
    scof_right = ss.oaconvolve(scof_frame, IR_right, mode='full') + add_leftover[1]
    
    add_leftover[0] = np.append(scof_left[2**10:], [0] * 2**10)
    add_leftover[1] = np.append(scof_right[2**10:], [0] * 2**10)

    scof_left = scof_left[:2**10]
    scof_right = scof_right[:2**10]

    ret_data = np.empty((scof_left.size + scof_right.size), dtype=scof_left.dtype)
    ret_data[1::2] = scof_left
    ret_data[0::2] = scof_right
    ret_data = ret_data.astype(np.float32).tostring()
    count += 1
    return (ret_data, pyaudio.paContinue)

# open stream using callback (3)
stream = p.open(format=pyaudio.paFloat32,
                channels=2,
                rate=int(scof_rate),
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