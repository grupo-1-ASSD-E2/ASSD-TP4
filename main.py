from processing_api_3D.HRIRs_interpreter.HRIRs_interpreter import *
import matplotlib.pyplot as plt
import time



if __name__ == "__main__":
    HRIR_interpreter = HRIRsInterpreter()
    IR = HRIR_interpreter.get_IR(110.0,10.0,4)
    fig, ax = plt.subplots(figsize=(15, 9))
    HRIR_interpreter.SOFA_change('./Resources/SOFA_Databases/HUTUBS/HRIRs/pp4_HRIRs_measured.sofa')
    IR = HRIR_interpreter.get_IR(10.0,85.0,1)
    ax.plot(IR[0,:], label="left", linewidth=0.5,  marker='o', markersize=1)
    ax.plot(IR[1,:], label="right", linewidth=0.5,  marker='o', markersize=1)
    ax.grid()
    ax.legend()
    plt.show()
    
