import numpy as np


class HRIRs_interpreter:

'''
Class in charge of searching for the appropiate IR.
Returns: numpy array with the IR values.
'''

    def __init__(self,SOFA_filename='./Resources/SOFA_Databases/MIT/mit_kemar_normal_pinna.sofa'):
        #hacer en la incializacion listas/arrays con IR de cada cosa
        self.database_name = get_database_name()
        self. SOFA_filename = SOFA_filename
        


    def get_IR(self, azymuth_angle, elevation, distance):
        


    def SOFA_change(self, SOFA_filename):
        self.SOFA_filename = SOFA_filename


    def get_database_name(self):
        HRIR = sofa.SOFAFile( self SOFA_filename, 'r')
        SOFA_attributes = HRIR.getGlobalAttributesAsDict()


    def generate_



    