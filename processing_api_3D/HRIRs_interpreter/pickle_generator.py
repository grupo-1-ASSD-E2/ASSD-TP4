from HRIRs_interpreter import *
import pickle
import os


def cargar_datos(filename):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except (OSError, IOError) as e:
        return dict()

def guardar_datos(dic, filename):
    with open('./Resources/SOFA_Databases/ARI/DAT/' + filename, "wb") as f:
        pickle.dump(dic, f, protocol=pickle.HIGHEST_PROTOCOL)

directory = './Resources/SOFA_Databases/ARI/HRIRs'

HRIR_interpreter = HRIRsInterpreter()

for filename in os.listdir(directory):
    HRIR_interpreter.SOFA_change(filename)
    dat_filename = filename
    guardar_datos(HRIR_interpreter.IR_dictionary, dat_filename.replace(".sofa",".dat"))