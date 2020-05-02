import numpy as np
import scipy.io.wavfile as sw
import scipy.signal as ss

class Convolutioner:
    '''
    Provides methods for DSP in real time.
    Minimum requirements for working are a given impulse response (IR), and the length of the successive samples of the signal being processed (L)
    '''

    def __init__(self, IR, length_of_input):
        # M = size of IR
        self.M = len(self.IR)
        # L = size of input samples to process
        self.L = length_of_input


        

    def compute_IR(self, IR):
        self.IR = IR


    def conv_cycle(self, input, impulse_response, window='hanning'):
        input_w = self.apply_window(input, window)
        # Zero padding input so that the FFT matches the size of the TF being used.
        inpt_fft = np.fft.fft(np.append(input, [0] * (self.M - 1)))


    def apply_window(self, signal, window='boxcar'):
        ''' window can be: 
            'boxcar' (rectangle),
            'barthann' (Bartlett-Hann), 
            'bartlett',
            'hanning', 
            'hamming',
            'tukey',
            'flattop',
            'hann',
            'nuttall',
            'parzen',
            'cosine',
            'blackman',
            'bohman',
            'blackmanharris' '''

        try:
            window = getattr(ss, window)(len(signal))
            signal_windowed = np.multiply(signal, window)
        except AttributeError:
            return None

        return signal_windowed