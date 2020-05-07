import numpy as np
import scipy.io.wavfile as sw
import scipy.signal as ss
import pyaudio

class Convolutioner:
    '''
    Provides methods for DSP in real time.
    Minimum requirements for working are a given impulse response (IR), and the length of the successive samples of the signal being processed (L).
    Overlap and save method is used since it requires no zero padding.
    input_array is the audio to be processed. Must be array-like (1D or 2D).
    
    IR_left, IR_right are the impulse response of the filter which will be used to process left and right channels, respectively. Must be array-like (1D or 2D). 
    If both are the same, the sound will be same as mono, if different, stereo.
    If IR_left and IR_right are 1D, it will be assumed that all tracks in input_array are to be processed by the same IR_left and IR_right.
    If IR_left and IR_right are 2D and have the same amount of rows as input_array, it means that not all the IRs should be the same, and therefore each track will be processed by the corresponding IR of the same row.
    If IR_left and IR_right are 2D but have a smaller amount of rows than the input_array, the remaining rows will be assumed to be a delta (and as such, the track will exit as it entered).
    If IR_left and IR_right are 2D but have a larger amount of rows from input_array, the exceeding rows will be ignored.
    '''

    def __init__(self, IR_left=np.ones(1), IR_right=np.ones(1), input_array=np.array([])):
        self.set_input(input_array)

        self.compute_IR(IR_left, IR_right)

        # Keeps count of the frames processed by the callback in non blocking mode.
        self.cycle_count = 0
        # Output data as an ndarray, where each row is a track in the song/sound.
        self.output_array = np.array([])
        # If True, output is saved to self.output_array
        self.save_output = False
        # Determines gain of added tracks when mixing them (generally <1)
        

        #todo self.output_fft = np.zeros(self.L + self.M - 1)
        #todo self.output = np.zeros(self.L + self.M - 1)
        

    def compute_IR(self, IR_left, IR_right):
        # Impulse Response for the left channel
        self.IR_left = np.array(IR_left)
        self.IR_left = self.reshape_IR(self.IR_left)

        # Impulse Response for the right channel
        self.IR_right = IR_right
        self.IR_right = self.reshape_IR(self.IR_right)

        # M = size of IR_left.
        self.M_left = self.IR_left.shape[1]
        # M = size of IR_right.
        self.M_right = self.IR_right.shape[1]
        # Transfer Function: DFT of the impulse response.
        self.TF_left = np.fft.fft(self.IR_left, self.L + self.M_left - 1)
        self.TF_right = np.fft.fft(self.IR_right, self.L + self.M_right - 1)
        
        # When working with non blocking mode, this saves the last elements of the previos frame processed to add them to the first elements of the new frame processed (overlap and add)
        self.leftover_left = np.zeros((self.tracks_num, self.L + self.M_left - 1), dtype=self.input_array.dtype)
        self.leftover_right = np.zeros((self.tracks_num, self.L + self.M_right - 1), dtype=self.input_array.dtype)


    def reshape_IR(self, IR):
        if IR.ndim == 1:
            # If it's 1D, it gets reshaped to match this class methods syntax.
            IR_ret = IR
            # Repeating IR for every track.
            for i in range(self.input_array.shape[0] - 1):
                IR_ret = np.vstack(IR_ret, IR)

        elif IR.shape[0] < self.input_array.shape[0]:
            # Filling the IR with deltas
            IR_ret = IR
            deltas_to_add = self.input_array.shape[0] - IR.shape[0]
            IR_delta = np.hstack((1 * np.ones((deltas_to_add, 1), dtype=IR.dtype), np.zeros((deltas_to_add, IR.shape[1] - 1), dtype=IR.dtype)))
            IR_ret = np.vstack(IR_ret, IR_delta)

        else:
            IR_ret = IR

        return IR_ret


    def set_input(self, tracks):
        '''
        tracks_to_add must be an ndarray containint the tracks as rows.
        '''
        # Input data to process as an ndarray, where each row is a track in the song/sound.
        self.input_array = np.array(tracks)
        if self.input_array.ndim == 1:
            self.input_array = np.reshape(self.input_array, (1, tracks.size))
            
        self.adjust_to_new_input()


    def add_tracks_to_input(self, tracks_to_add):
        '''
        tracks_to_add must be an ndarray containint the tracks as rows.
        '''
        self.input_array = np.vstack(self.input_array, tracks_to_add)
        self.adjust_to_new_input()


    def adjust_to_new_input(self):
        '''
        Adjusts class variables to new input.
        '''
        # Number of tracks, a.k.a. number of rows in self.input_array.
        self.tracks_num = self.input_array.shape[0]
        # Number of tracks to process, i.e. number of row in self.input_array.
        self.L = self.input_array.shape[1]


    def adjust_mixing_gain(self):
        '''
        Determines optimum gain to apply to the mixing of tracks.
        '''
        #TODO MAKE THIS PROPERLY: THis is hardcoded for HUTUBS HRIRs.
        self.mixing_gain = 2**(-3)


    def pyaudio_callback(self, in_data, frame_count, time_info, status):
        '''
        callback method to be called by PyAudio in non blocking mode.
        '''
        audio_size = np.shape(self.input_array)[1]
        if frame_count*self.cycle_count > audio_size:
            # Processing is complete.
            return (None, pyaudio.paComplete)
        elif frame_count*(self.cycle_count+1) > audio_size:
            # Last frame to process.
            frames_left = audio_size - frame_count*self.cycle_count
        else:
            # Every other frame.
            frames_left = frame_count

        audio_frame = np.hstack((self.input_array[:, frame_count*self.cycle_count : frame_count*self.cycle_count + frames_left], 
                                np.zeros((self.tracks_num, frame_count - frames_left), 
                                dtype=self.input_array.dtype)))

        # Setting up output arrays.
        audio_frame_left = np.zeros((self.tracks_num, self.L + self.M_left - 1), dtype=audio_frame.dtype)
        audio_frame_right = np.zeros((self.tracks_num, self.L + self.M_right - 1), dtype=audio_frame.dtype)

        # Processing each track of the frame using the scipy overlap and add convolution, but also performing overlap and on the whole thing since we are processing the input by frames.
        for i in range(audio_frame.shape[0]):
            audio_frame_left[i]  = ss.oaconvolve(audio_frame[i], self.IR_left[i], mode='full') + self.leftover_left[i]
            audio_frame_right[i] = ss.oaconvolve(audio_frame[i], self.IR_right[i], mode='full') + self.leftover_right[i]
    
        # Saving last self.M - 1 elements for next cycle.
        self.leftover_left = np.hstack((audio_frame_left[:, frame_count:], np.zeros((self.tracks_num, frame_count), dtype=audio_frame.dtype)))
        self.leftover_right = np.hstack((audio_frame_right[:, frame_count:], np.zeros((self.tracks_num, frame_count), dtype=audio_frame.dtype)))

        # Discarding last self.M - 1 elements.
        audio_frame_left = audio_frame_left[:, :frame_count]
        audio_frame_right = audio_frame_right[:, :frame_count]

        # Mixing tracks.
        audio_frame_left = self.mixing_gain * np.sum(audio_frame_left, axis=0)
        audio_frame_right = self.mixing_gain * np.sum(audio_frame_right, axis=0)
    
        # Preparing data to send to PyAudio.
        out_data = np.empty((audio_frame_left.size + audio_frame_right.size), dtype=audio_frame.dtype)
        # Odd elements are going to the left channel.
        out_data[1::2] = audio_frame_left
        # Even elements are going to the right channel.
        out_data[0::2] = audio_frame_right

        
        ret_data = out_data.tostring()

        self.cycle_count += 1
        
        return (ret_data, pyaudio.paContinue)


    # def conv_cycle(self, input_signal, impulse_response):
    #     # Zero padding input so that the FFT matches the size of the TF being used.
    #     input_fft = np.fft.fft(input_signal)

    #     self.output_fft = np.multiply(input_fft, self.TF)
    #     self.output = np.fft.ifft(self.output_fft)
    #     return self.output