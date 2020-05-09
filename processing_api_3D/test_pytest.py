import scipy.signal as ss
import numpy as np
import time
import librosa
import pysofaconventions as sofa
from audio_processing.convolutioner import Convolutioner

def test_convolve(capsys):
    '''
    Tests the speed of different convolutions.
    '''
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


def test_moving_br():
    '''
    Test Convolutioner when audio is playing and output changes every TEMP seconds.
    '''
    TEMP = 1
    hrir = sofa.SOFAFile('././Resources/SOFA_Databases/HUTUBS/HRIRs/pp1_HRIRs_measured.sofa', 'r') #'././Resources/SOFA_Databases/ARI/HRIRs/hrtf_nh2.sofa'
    IRs_left = np.vstack((
        hrir.getDataIR()[211,0,:], 
        hrir.getDataIR()[175,0,:],
        hrir.getDataIR()[139,0,:],
        hrir.getDataIR()[103,0,:],
        hrir.getDataIR()[71,0,:],
        hrir.getDataIR()[27,0,:],
        hrir.getDataIR()[2,0,:],
        hrir.getDataIR()[0,0,:],
        hrir.getDataIR()[6,0,:],
        hrir.getDataIR()[18,0,:],
        hrir.getDataIR()[35,0,:],
        hrir.getDataIR()[58,0,:],
        hrir.getDataIR()[86,0,:],
        hrir.getDataIR()[121,0,:],
        hrir.getDataIR()[157,0,:],
        hrir.getDataIR()[193,0,:],
        hrir.getDataIR()[229,0,:],
        hrir.getDataIR()[265,0,:],
        hrir.getDataIR()[301,0,:],
        hrir.getDataIR()[337,0,:],
        hrir.getDataIR()[369,0,:],
        hrir.getDataIR()[394,0,:],
        hrir.getDataIR()[414,0,:],
        hrir.getDataIR()[429,0,:],
        hrir.getDataIR()[438,0,:],
        hrir.getDataIR()[439,0,:],
        hrir.getDataIR()[434,0,:],
        hrir.getDataIR()[422,0,:],
        hrir.getDataIR()[404,0,:],
        hrir.getDataIR()[382,0,:],
        hrir.getDataIR()[353,0,:],
        hrir.getDataIR()[319,0,:],
        hrir.getDataIR()[283,0,:],
        hrir.getDataIR()[247,0,:]
    ))
    IRs_right = np.vstack((
        hrir.getDataIR()[211,1,:], 
        hrir.getDataIR()[175,1,:],
        hrir.getDataIR()[139,1,:],
        hrir.getDataIR()[103,1,:],
        hrir.getDataIR()[71,1,:],
        hrir.getDataIR()[27,1,:],
        hrir.getDataIR()[2,1,:],
        hrir.getDataIR()[0,1,:],
        hrir.getDataIR()[6,1,:],
        hrir.getDataIR()[18,1,:],
        hrir.getDataIR()[35,1,:],
        hrir.getDataIR()[58,1,:],
        hrir.getDataIR()[86,1,:],
        hrir.getDataIR()[121,1,:],
        hrir.getDataIR()[157,1,:],
        hrir.getDataIR()[193,1,:],
        hrir.getDataIR()[229,1,:],
        hrir.getDataIR()[265,1,:],
        hrir.getDataIR()[301,1,:],
        hrir.getDataIR()[337,1,:],
        hrir.getDataIR()[369,1,:],
        hrir.getDataIR()[394,1,:],
        hrir.getDataIR()[414,1,:],
        hrir.getDataIR()[429,1,:],
        hrir.getDataIR()[438,1,:],
        hrir.getDataIR()[439,1,:],
        hrir.getDataIR()[434,1,:],
        hrir.getDataIR()[422,1,:],
        hrir.getDataIR()[404,1,:],
        hrir.getDataIR()[382,1,:],
        hrir.getDataIR()[353,1,:],
        hrir.getDataIR()[319,1,:],
        hrir.getDataIR()[283,1,:],
        hrir.getDataIR()[247,1,:]
    ))


    input_files = [
        './Resources/Audio files/Multitracks Bohemian Rhapsody/01 - Borap01.mp3',
        './Resources/Audio files/Multitracks Bohemian Rhapsody/02 - Borap02.mp3',
        './Resources/Audio files/Multitracks Bohemian Rhapsody/03 - Borap03.mp3',
        './Resources/Audio files/Multitracks Bohemian Rhapsody/04 - Borap04.mp3',
        './Resources/Audio files/Multitracks Bohemian Rhapsody/05 - Borap05.mp3',
    ]

    conv = Convolutioner(IRs_left[0], IRs_right[0], input_files)
    conv.start_non_blocking_processing()

    count = 0
    while conv.processing():
        count += 1
        conv.compute_IR(IRs_left[count], IRs_right[count])
        time.sleep(TEMP)

    conv.terminate_processing()
    conv.get_output_file('/tests_output/moving_br.wav')