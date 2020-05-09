import time
import numpy as np
from audio_processing.convolutioner import Convolutioner
from HRIRs_interpreter.HRIRs_interpreter import HRIRsInterpreter

HRIR = HRIRsInterpreter(SOFA_filename='././Resources/SOFA_Databases/ARI/HRIRs/hrtf_nh2.sofa')
IRs = HRIR.get_IR(90.0, 0.0, 1)

conv = Convolutioner(IRs[0], IRs[1])
br = np.load('processing_api_3D/tests output/Bohemian Rhapsody ndarray.npy')
conv.update_input(br, tracks_dtype=conv.input_array.dtype)

conv.start_non_blocking_processing()

elevation_angle = 0.0
while conv.processing():
    if elevation_angle < 90.0:
        IRs.get_IR(90.0, elevation_angle, 1)
        elevation_angle += 5.0
    
    elif elevation_angle == 90.0:
        IRs.get_IR(0.0, elevation_angle, 1)
        elevation_angle += 5.0

    elif elevation_angle > 90.0:
        IRs.get_IR(-90.0, elevation_angle, 1)
        elevation_angle += 5.0

    conv.compute_IR(IRs[0], IRs[1])
    time.sleep(2)

conv.terminate_processing()
conv.save_output_array('processing_api_3D/tests output/moving_br_ndarray.npy')
conv.get_output_file('processing_api_3D/tests output/moving_br.wav')