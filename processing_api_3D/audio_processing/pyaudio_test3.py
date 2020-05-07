"""PyAudio Example: Play a wave file (callback version)."""

import pyaudio
import time
import sys
import pysofaconventions as sofa
import scipy.signal as ss
import scipy.fft as sf
import numpy as np
import librosa

br1_data, br1_rate = librosa.load('././Resources/Audio files/Multitracks Bohemian Rhapsody/01 - Borap01.mp3', sr=44.1e3, dtype=np.float32)
br2_data, br2_rate = librosa.load('././Resources/Audio files/Multitracks Bohemian Rhapsody/02 - Borap02.mp3', sr=44.1e3, dtype=np.float32)
br3_data, br3_rate = librosa.load('././Resources/Audio files/Multitracks Bohemian Rhapsody/03 - Borap03.mp3', sr=44.1e3, dtype=np.float32)

max_size_br = max(br1_data.size, br2_data.size, br3_data.size)

br_data = np.vstack((np.append(br1_data, np.zeros(max_size_br - br1_data.size, dtype=br1_data.dtype)), np.append(br2_data, np.zeros(max_size_br - br2_data.size, dtype=br1_data.dtype)), np.append(br3_data, np.zeros(max_size_br - br3_data.size, dtype=br1_data.dtype))))
print(br_data.dtype)
print(br_data.size)
hrir = sofa.SOFAFile('././Resources/SOFA_Databases/HUTUBS/HRIRs/pp1_HRIRs_measured.sofa', 'r') #'././Resources/SOFA_Databases/ARI/HRIRs/hrtf_nh2.sofa'
print(hrir.getDataIR()[205,0,:].dtype)

# instantiate PyAudio (1)
p = pyaudio.PyAudio()
count = 0
IR_left = hrir.getDataIR()[209,0,:].astype(np.float32)
IR_left = np.vstack((IR_left, IR_left, IR_left))
TF_left = sf.rfftn(IR_left, 2**10 + 2**8 - 1)
IR_right = hrir.getDataIR()[209,1,:].astype(np.float32)
IR_right = np.vstack((IR_right, IR_right, IR_right))
TF_right = sf.rfftn(IR_right, 2**10 + 2**8 - 1)
print(IR_left.shape)

IR_delta = np.hstack((2 * np.ones((3, 1), dtype=IR_left.dtype), np.zeros((3, 2**8 - 1), dtype=IR_left.dtype)))

add_leftover = np.zeros((6, 2**10 + 2**8 - 1), dtype=np.float32)

# define callback (2)
def callback(in_data, frame_count, time_info, status):
    global count

    audio_size = np.shape(br_data)[1]
    if frame_count*count > audio_size:
        return (None, pyaudio.paComplete)
    elif frame_count*(count+1) > audio_size:
        frames_left = audio_size - frame_count*count
    else:
        frames_left = frame_count
    
    br_frame = np.hstack((br_data[:, frame_count*count : frame_count*count + frames_left], np.zeros((3, frame_count - frames_left), dtype=br_data.dtype)))
    # br_left = np.add(ss.oaconvolve(br_frame, IR_left, mode='full')[:3], add_leftover[:3])
    # br_right = np.add(ss.oaconvolve(br_frame, IR_right, mode='full')[:3], add_leftover[3:])


    # conv_left = sf.irfftn(np.multiply(TF_left, sf.rfftn(br_frame, 2**10 + 2**8 - 1)), 2**10 + 2**8 - 1)
    # conv_right = sf.irfftn(np.multiply(TF_right, sf.rfftn(br_frame, 2**10 + 2**8 - 1)), 2**10 + 2**8 - 1)

    # br_left = np.add(conv_left, add_leftover[:3])
    # br_right = np.add(conv_right, add_leftover[3:])


    br_left = np.zeros((3, 2**10 + 2**8 - 1), dtype=br_frame.dtype)
    br_right = np.zeros((3, 2**10 + 2**8 - 1), dtype=br_frame.dtype)
    # br_left[0] = ss.oaconvolve(br_frame[0], IR_left[0], mode='full') + add_leftover[0]
    # br_right[0] = ss.oaconvolve(br_frame[0], IR_right[0], mode='full') + add_leftover[3]
    # br_left[1] = ss.oaconvolve(br_frame[1], IR_left[1], mode='full') + add_leftover[1]
    # br_right[1] = ss.oaconvolve(br_frame[1], IR_right[1], mode='full') + add_leftover[4]
    # br_left[2] = ss.oaconvolve(br_frame[2], IR_left[2], mode='full') + add_leftover[2]
    # br_right[2] = ss.oaconvolve(br_frame[2], IR_right[2], mode='full') + add_leftover[5]

    for i in range(br_frame.shape[0]):
        aux_left = ss.oaconvolve(br_frame[i], IR_left[i], mode='full')
        br_left[i] = aux_left + add_leftover[i]
        aux_right = ss.oaconvolve(br_frame[i], IR_right[i], mode='full')
        br_right[i] = aux_right + add_leftover[i+3]
    
    add_leftover[:3] = np.hstack((br_left[:, 2**10:], np.zeros((3, 2**10), dtype=np.float32)))
    add_leftover[3:] = np.hstack((br_right[:, 2**10:], np.zeros((3, 2**10), dtype=np.float32)))

    br_left = br_left[:, :2**10]
    br_right = br_right[:, :2**10]

    br_left = 2**(-3) * (br_left[0,:] + br_left[1,:] + br_left[2,:])
    br_right = 2**(-3) * (br_right[0,:] + br_right[1,:] + br_right[2,:])
    # br_left = br_left[0,:]
    # br_right = br_right[0,:]
   
    ret_data = np.empty((br_left.size + br_right.size), dtype=br_left.dtype)
    ret_data[1::2] = br_left
    ret_data[0::2] = br_right
    ret_data = ret_data.tostring()
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
        IR_left = hrir.getDataIR()[209,0,:].astype(np.float32) #6
        IR_left = np.vstack((IR_left, IR_left, IR_left))
        TF_left = sf.rfftn(IR_left, 2**10 + 2**8 - 1)
        IR_right = hrir.getDataIR()[209,1,:].astype(np.float32) #6
        IR_right = np.vstack((IR_right, IR_right, IR_right))
        TF_right = sf.rfftn(IR_right, 2**10 + 2**8 - 1)
    elif while_count % 3 == 1:
        IR_left = hrir.getDataIR()[205,0,:].astype(np.float32) #396
        IR_left = np.vstack((IR_left, IR_left, IR_left))
        TF_left = sf.rfftn(IR_left, 2**10 + 2**8 - 1)
        IR_right = hrir.getDataIR()[205,1,:].astype(np.float32) #396
        IR_right = np.vstack((IR_right, IR_right, IR_right))
        TF_right = sf.rfftn(IR_right, 2**10 + 2**8 - 1)
    elif while_count % 3 == 2:
        IR_left = hrir.getDataIR()[227,0,:].astype(np.float32) #1029
        IR_left = np.vstack((IR_left, IR_left, IR_left))
        TF_left = sf.rfftn(IR_left, 2**10 + 2**8 - 1)
        IR_right = hrir.getDataIR()[227,1,:].astype(np.float32) #1029
        IR_right = np.vstack((IR_right, IR_right, IR_right))
        TF_right = sf.rfftn(IR_right, 2**10 + 2**8 - 1)

    time.sleep(26)

# stop stream (6)
stream.stop_stream()
stream.close()

# close PyAudio (7)
p.terminate()