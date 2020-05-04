"""PyAudio Example: Play a wave file (callback version)."""

import pyaudio
import wave
import time
import sys
import pysofaconventions as sofa
import scipy.signal as ss
import scipy.io.wavfile as sw
import numpy as np
import wavio

br3 = wave.open('C:/Users/facun/OneDrive/Desktop/ITBA/6C ASSD/ASSD-TP4/Resources/Audio files/Multitracks Bohemian Rhapsody/03 - Borap03.wav', 'rb')
hrir = sofa.SOFAFile('C:/Users/facun/OneDrive/Desktop/ITBA/6C ASSD/ASSD-TP4/Resources/SOFA_Databases/HUTUBS/HRIRs/pp1_HRIRs_measured.sofa', 'r')

# instantiate PyAudio (1)
p = pyaudio.PyAudio()

# define callback (2)
def callback(in_data, frame_count, time_info, status):
    # br3_left = ss.fftconvolve(np.asarray(np.frombuffer(br3.readframes(frame_count), dtype=np.float32)), hrir.getDataIR()[209,0,:])
    # br3_right = ss.fftconvolve(np.asarray(np.frombuffer(br3.readframes(frame_count), dtype=np.float32)), hrir.getDataIR()[209,1,:])
    # br3_right = np.fromstring(br3.readframes(frame_count), dtype=np.float32)
    # data = np.empty((br3_left.size + br3_right.size), dtype=br3_left.dtype)
    # data[0::2] = br3_left
    # data[1::2] = br3_right
    data = br3.readframes(frame_count)
    br3_array = wavio._wav2array(br3.getnchannels(), br3.getsampwidth(), data)
    ret_data = br3_array.astype(np.int16).tostring()
    return (ret_data, pyaudio.paContinue)

# open stream using callback (3)
stream = p.open(format=p.get_format_from_width(br3.getsampwidth()),
                channels=1,
                rate=br3.getframerate(),
                output=True,
                stream_callback=callback)

# start the stream (4)
stream.start_stream()

# wait for stream to finish (5)
while stream.is_active():
    time.sleep(0.1)

# stop stream (6)
stream.stop_stream()
stream.close()
br3.close()

# close PyAudio (7)
p.terminate()