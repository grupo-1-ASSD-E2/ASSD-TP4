import numpy as np
import pysofaconventions as sofa
from pysofaconventions import *

class HRIRsInterpreter:

'''
Class in charge of searching for the appropiate IR.
Returns: numpy array with the IR values.
'''

    def __init__(self,SOFA_filename='./Resources/SOFA_Databases/MIT/mit_kemar_normal_pinna.sofa'):
        #hacer en la incializacion listas/arrays con IR de cada cosa
        self.SOFA_filename = SOFA_filename
        set_database_name()
        self.HRIR_SOFA_file = sofa.SOFAFile( self.SOFA_filename, 'r')



    def set_IR(self, azymuth_angle, elevation, distance):
        if self.database_name = 'HUTUBS':
            elevation_difference = elevation % 10
            if elevation_difference < 5:
                real_elevation = elevation - elevation_difference
            else:
                real_elevation = elevation + 10 - elevation_difference

        elif self.database_name = 'CIPIC':
            


    def SOFA_change(self, SOFA_filename):
        self.SOFA_filename = SOFA_filename
        self.HRIR_SOFA_file = sofa.SOFAFile( self.SOFA_filename, 'r')
        set_database_name()

    def set_database_name(self):
        SOFA_attributes = HRIR.getGlobalAttributesAsDict()
        self.database_name = SOFA_attributes['DatabaseName']

    def set_SOFA_conventions(self):
        convention = file.getGlobalAttributeValue("SOFAConventions")
        if convention == 'AmbisonicsDRIR':
            conventionFile = SOFAAmbisonicsDRIR(self.SOFA_filename,"r")
        elif convention == 'GeneralFIR':
            conventionFile = SOFAGeneralFIR(self.SOFA_filename,"r")
        elif convention == 'GeneralFIRE':
            conventionFile = SOFAGeneralFIRE(self.SOFA_filename,"r")
        elif convention == 'GeneralTF':
            conventionFile = SOFAGeneralTF(self.SOFA_filename,"r")
        elif convention == 'MultiSpeakerBRIR':
            conventionFile = SOFAMultiSpeakerBRIR(self.SOFA_filename,"r")
        elif convention == 'SimpleFreeFieldHRIR':
            conventionFile = SOFASimpleFreeFieldHRIR(self.SOFA_filename,"r")
        elif convention == 'SimpleFreeFieldSOS':
            conventionFile = SOFASimpleFreeFieldSOS(self.SOFA_filename,"r")
        elif convention == 'SimpleHeadphoneIR':
            conventionFile = SOFASimpleHeadphoneIR(self.SOFA_filename,"r")
        elif convention == 'SingleRoomDRIR':
            conventionFile = SOFASingleRoomDRIR(self.SOFA_filename,"r")
        else:
            raise internal_error("Wrong SOFA convention")
        self.SOFA_convention = conventionFile

    def set_SOFA_sampling_rate(self):
        self.sampling_rate = self.SOFA_convention.getSamplingRate() #Sampling rate ends with . i.e: '44100.'

    
    
    def generate_HRIR_dictionary(self):





class InternalError(Exception):

    def __init__(self, message):
        self.message = message




    