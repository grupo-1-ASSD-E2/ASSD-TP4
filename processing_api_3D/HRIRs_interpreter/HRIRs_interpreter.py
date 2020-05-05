import numpy as np
import pysofaconventions as sofa
from pysofaconventions import *

class HRIRsInterpreter:

    '''
    Class in charge of searching for the appropiate IR.
    Returns: numpy array with the IR values.
    '''

    def __init__(self,SOFA_filename='./Resources/SOFA_Databases/ARI/HRIRs/hrtf_nh2.sofa'):#Subject 1 is a Kemar doll in HUTUBS
        self.SOFA_filename = SOFA_filename
        self.HRIR_SOFA_file = sofa.SOFAFile( self.SOFA_filename, 'r')
        self.set_database_name()
        self.create_IR_dictionary()


    def get_IR(self, azimuth_angle, elevation, distance):
        self.interpolate_elevation(elevation)
        self.interpolate_azimuth_angle(azimuth_angle)
        aux_IR = np.array((self.IR_dictionary[str(self.real_elevation)][str(self.real_azimuth_angle)]['Left'], self.IR_dictionary[str(self.real_elevation)][str(self.real_azimuth_angle)]['Right']))
        self.adjust_to_distance(distance, aux_IR)
        return self.required_IR

    def create_IR_dictionary(self):
        ''' 
        This method creates nested dictionaries. 
        The first one classifies by elevation, then by 
        azimuth angle and finally by Right or Left ear.
        e.g.:Elevaton 80° azimuth 0° left ear is 
        IR_dictionary['80']['0']['Left']
        '''
        self.IR_dictionary = {}
        if self.database_name == 'HUTUBS':
            for elev in range(90,-100,-10):
                if elev == 90:
                    pos = np.arange(0,1)
                elif elev == 80:
                    pos = np.arange(1,7)
                elif elev == 70:
                    pos = np.arange(7,22)
                elif elev == 60:
                    pos = np.arange(22,40)
                elif elev == 50:
                    pos = np.arange(40,64)
                elif elev == 40:
                    pos = np.arange(64,94)
                elif elev == 30:
                    pos = np.arange(94,130)
                elif elev == 20:
                    pos = np.arange(130,166)
                elif elev == 10:
                    pos = np.arange(166,202)
                elif elev == 0:
                    pos = np.arange(202,238)
                elif elev == -10:
                    pos = np.arange(238,274)
                elif elev == -20:
                    pos = np.arange(274,310)
                elif elev == -30:
                    pos = np.arange(310,346)
                elif elev == -40:
                    pos = np.arange(346,376)
                elif elev == -50:
                    pos = np.arange(376,400)
                elif elev == -60:
                    pos = np.arange(400,418)
                elif elev == -70:
                    pos = np.arange(418,433)
                elif elev == -80:
                    pos = np.arange(433,439)
                elif elev == -90:
                    pos = np.arange(439,440)

                self.IR_dictionary.update({str(elev): {} })
                for j in pos:
                    self.IR_dictionary[str(elev)].update({str(int(self.HRIR_SOFA_file.getVariableValue('SourcePosition')[j,0])): { 'Left': np.array(self.HRIR_SOFA_file.getDataIR()[j,0,:]), 'Right': np.array(self.HRIR_SOFA_file.getDataIR()[j,1,:])}})
                
        elif self.database_name == 'ARI':
            sorted_IR = np.array(self.HRIR_SOFA_file.getVariableValue('SourcePosition'))
            samples = np.shape(sorted_IR)[0]
            index = np.reshape(np.arange(0,samples),(samples,1))
            sorted_IR = np.hstack((sorted_IR,index))
            sorted_IR = np.delete(sorted_IR,2,1)
            sorted_IR.view('float,float,float').sort(order=['f1'], axis=0)
            count = 0
            for elev in range(-30,85,5):
                elev_f = float(elev)
                self.IR_dictionary.update({str(elev_f): {} })
                for j in range(count,samples,1):
                    if elev_f == sorted_IR[j,1]:
                        self.IR_dictionary[str(elev_f)].update({str(self.HRIR_SOFA_file.getVariableValue('SourcePosition')[int(sorted_IR[j,2]),0]): { 'Left': np.array(self.HRIR_SOFA_file.getDataIR()[int(sorted_IR[j,2]),0,:]), 'Right': np.array(self.HRIR_SOFA_file.getDataIR()[int(sorted_IR[j,2]),1,:])}})
                        count +=1    
                    else:
                        break
                
    def interpolate_elevation(self, elevation):
        '''
        This method interpolates the elevation required 
        to the closest value.
        '''

        if self.database_name == 'HUTUBS':
            #HUTUBS database has measures with elevation resolution of 10°
            resolution = 10
            elevation_int = int(elevation)
            elevation_difference = elevation_int % resolution

            if elevation_difference == 0:
                self.real_elevation = elevation_int 
            elif elevation_difference < resolution / 2:
                self.real_elevation = elevation_int - elevation_difference
            else:
                self.real_elevation = elevation_int + resolution - elevation_difference

        elif self.database_name == 'ARI':
            #ARI database has measures with elevation resolution of 5°
            resolution = 5
            elevation_difference = elevation % resolution

            if elevation_difference == 0:
                self.real_elevation = elevation 
            elif elevation_difference < resolution / 2:
                self.real_elevation = elevation - elevation_difference
            else:
                self.real_elevation = elevation + resolution - elevation_difference

    def interpolate_azimuth_angle(self,azimuth_angle):
        if self.database_name == 'HUTUBS':
            azimuth_angle_int = int(azimuth_angle)
            #Azimuth angle resolution in HUTUBS varies depending on the elevation
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
            azimuth_difference = azimuth_angle_int % resolution

            if azimuth_difference == 0:
                self.real_azimuth_angle = azimuth_angle_int
            elif azimuth_difference < resolution / 2:
                self.real_azimuth_angle = azimuth_angle_int - azimuth_difference
            else:
                self.real_azimuth_angle = azimuth_angle_int - azimuth_difference + resolution
            if self.real_azimuth_angle == 360:
                self.real_azimuth_angle = 0

        elif self.database_name == 'ARI':
            #Azimuth angle resolution in ARI is constantly 2.5°
            resolution = 2.5
            azimuth_difference = azimuth_angle % resolution

            if azimuth_difference == 0:
                self.real_azimuth_angle = azimuth_angle 
            elif azimuth_difference < resolution / 2:
                self.real_azimuth_angle = azimuth_angle - azimuth_difference
            else:
                self.real_azimuth_angle = azimuth_angle + resolution - azimuth_difference
            
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
        self.database_name = self.HRIR_SOFA_file.getGlobalAttributeValue('DatabaseName')

    def set_SOFA_conventions(self):
        convention = self.HRIR_SOFA_file.getGlobalAttributeValue("SOFAConventions")
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
        self.sampling_rate = self.HRIR_SOFA_file.getSamplingRate() 

    



class InternalError(Exception):

    def __init__(self, message):
        self.message = message




    