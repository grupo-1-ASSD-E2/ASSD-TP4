import numpy as np
import pysofaconventions as sofa
from pysofaconventions import *

class HRIRsInterpreter:

    '''
    Class in charge of searching for the appropiate IR.
    Returns: numpy array with the IR values.
    '''

    def __init__(self,SOFA_filename='./Resources/SOFA_Databases/HUTUBS/HRIRs/pp1_HRIRs_measured.sofa'):
        self.SOFA_filename = SOFA_filename
        self.HRIR_SOFA_file = sofa.SOFAFile( self.SOFA_filename, 'r')
        self.set_database_name()
        self.create_IR_dictionary()


    def get_IR(self, azimuth_angle, elevation, distance):
        if self.database_name == 'HUTUBS':
            self.interpolate_elevation(elevation)
            self.interpolate_azimuth_angle(azimuth_angle)
            aux_IR = np.array((self.IR_dictionary[str(self.real_elevation)][str(self.real_azimuth_angle)]['Left'], self.IR_dictionary[str(self.real_elevation)][str(self.real_azimuth_angle)]['Right']))
            self.adjust_to_distance(distance, aux_IR)
            return self.required_IR

    def create_IR_dictionary(self):
        ''' 
        This method creates nested dictionaries. 
        The first one classifies by elevation, then by azimuth angle and finally by Right or Left ear.
        e.g.:Elevaton 80° azimuth 0° left ear is IR_dictionary['80']['0']['Left']
        '''
        self.IR_dictionary = {}
        for i in range(90,-100,-10):
            if i == 90:
                k=1
                pos = np.arange(0,1)
            elif i == 80:
                k=6
                pos = np.arange(1,7)
            elif i == 70:
                k=15
                pos = np.arange(7,22)
            elif i == 60:
                k=18
                pos = np.arange(22,40)
            elif i == 50:
                k=24
                pos = np.arange(40,64)
            elif i == 40:
                k=30
                pos = np.arange(64,94)
            elif i == 30:
                k=36
                pos = np.arange(94,130)
            elif i == 20:
                k=36
                pos = np.arange(130,166)
            elif i == 10:
                k=36
                pos = np.arange(166,202)
            elif i == 0:
                k=36
                pos = np.arange(202,238)
            elif i == -10:
                k=36
                pos = np.arange(238,274)
            elif i == -20:
                k=36
                pos = np.arange(274,310)
            elif i == -30:
                k=36
                pos = np.arange(310,346)
            elif i == -40:
                k=30
                pos = np.arange(346,376)
            elif i == -50:
                k=24
                pos = np.arange(376,400)
            elif i == -60:
                k=18
                pos = np.arange(400,418)
            elif i == -70:
                k=15
                pos = np.arange(418,433)
            elif i == -80:
                k=6
                pos = np.arange(433,439)
            elif i == -90:
                k=1
                pos = np.arange(439,440)

            self.IR_dictionary.update({str(i): {} })
            for j in pos:
                self.IR_dictionary[str(i)].update({str(int(self.HRIR_SOFA_file.getVariableValue('SourcePosition')[j,0])): { 'Left': np.array(self.HRIR_SOFA_file.getDataIR()[j,0,:]), 'Right': np.array(self.HRIR_SOFA_file.getDataIR()[j,1,:])}})

        #elif self.database_name == 'CIPIC':

    def interpolate_elevation(self, elevation):
        if self.database_name == 'HUTUBS':
            #HUTUBS database has measures with elevation resolution of 10°
            elevation_difference = elevation % 10
            if elevation_difference == 0:
                self.real_elevation = elevation 
            elif elevation_difference < 5:
                self.real_elevation = elevation - elevation_difference
            else:
                self.real_elevation = elevation + 10 - elevation_difference

    def interpolate_azimuth_angle(self,azimuth_angle):
        if self.database_name == 'HUTUBS':
            if abs(self.real_elevation) == 90:
                resolution = 360
            elif abs(self.real_elevation) == 90:
                resolution = 60
            elif abs(self.real_elevation) == 90:
                resolution = 24
            elif abs(self.real_elevation) == 90:
                resolution = 20
            elif abs(self.real_elevation) == 90:
                resolution = 15
            elif abs(self.real_elevation) == 90:
                resolution = 12
            else:
                resolution = 10
            azimuth_difference = azimuth_angle % resolution

            if azimuth_difference == 0:
                self.real_azimuth_angle = azimuth_angle
            elif azimuth_difference < resolution / 2:
                self.real_azimuth_angle = azimuth_angle - azimuth_difference
            else:
                self.real_azimuth_angle = azimuth_angle - azimuth_difference + resolution
            if self.real_azimuth_angle == 360:
                self.real_azimuth_angle = 0
            
    def adjust_to_distance(self, distance, IR):
        self.database_distance = self.HRIR_SOFA_file.getVariableValue('SourcePosition')[0,2]
        adjustment_db = -6 * (distance - self.database_distance) / self.database_distance
        adjustment_times = 10 ** (adjustment_db / 20)
        self.required_IR = IR * adjustment_times

    def SOFA_change(self, SOFA_filename):
        self.SOFA_filename = SOFA_filename
        self.HRIR_SOFA_file = sofa.SOFAFile( self.SOFA_filename, 'r')
        self.set_SOFA_conventions()
        self.set_SOFA_sampling_rate()
        self.create_IR_dictionary()
        self.set_database_name()

    def set_database_name(self):
        SOFA_attributes = self.HRIR_SOFA_file.getGlobalAttributesAsDict()
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
        self.sampling_rate = self.SOFA_convention.getSamplingRate() #Sampling rate ends with . e.g.: '44100.'

    



class InternalError(Exception):

    def __init__(self, message):
        self.message = message




    