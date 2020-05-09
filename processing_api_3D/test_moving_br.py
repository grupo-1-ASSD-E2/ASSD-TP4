import time
import numpy as np
import pysofaconventions as sofa
from audio_processing.convolutioner import Convolutioner


'''
Test Convolutioner when audio is playing and output changes every given seconds seconds.
'''
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

conv = Convolutioner(IRs_left[0], IRs_right[0])
br = np.load('processing_api_3D/tests output/Bohemian Rhapsody ndarray.npy')
conv.update_input(br, tracks_dtype=conv.input_array.dtype)

conv.start_non_blocking_processing()

count = 0
while conv.processing():
    count += 1
    if count >= len(IRs_left):
        count = 0

    conv.compute_IR(IRs_left[count], IRs_right[count])
    time.sleep(2)

conv.terminate_processing()
conv.save_output_array('processing_api_3D/tests output/moving_br_ndarray.npy')
conv.get_output_file('processing_api_3D/tests output/moving_br.wav')