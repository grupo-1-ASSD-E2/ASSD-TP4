import scipy.signal as ss
import numpy as np
import time
import librosa
import pysofaconventions as sofa

def test_convolve(capsys):
    frame_count = 2**20
    br1_data, br1_rate = librosa.load('./Resources/Audio files/Multitracks Bohemian Rhapsody/01 - Borap01.mp3', sr=44.1e3, dtype=np.float32)
    hrir = sofa.SOFAFile('./Resources/SOFA_Databases/HUTUBS/HRIRs/pp1_HRIRs_measured.sofa', 'r')
    IR = hrir.getDataIR()[209,0,:].astype(np.float32)
    frame = br1_data[:frame_count]
    
    with capsys.disabled():
        print('Testing times for frame_count = {}'.format(frame_count))
    
    start_time = time.time()
    np.convolve(frame, IR)
    np_convolve_time = time.time()
    print("--- np.convolve took {:0.50f} seconds ---".format(np_convolve_time - start_time))

    ss.convolve(frame, IR)
    ss_convolve_time = time.time()
    print("--- ss.convolve took {:0.50f} seconds ---".format(ss_convolve_time - np_convolve_time))

    ss.fftconvolve(frame, IR)
    ss_fftconvolve_time = time.time()
    print("--- ss.fftconvolve took {:0.50f} seconds ---".format(ss_fftconvolve_time - ss_convolve_time))

    ss.oaconvolve(frame, IR)
    ss_oaconvolve_time = time.time()
    print("--- ss.oaconvolve took {:0.50f} seconds ---".format(ss_oaconvolve_time - ss_fftconvolve_time))

    assert False