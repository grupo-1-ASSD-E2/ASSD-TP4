import numpy as np
import scipy.io.wavfile as sw
import scipy.signal as ss

class Convolutioner:
    '''
    Provides methods for DSP in real time.
    Minimum requirements for working are a given impulse response (IR), and the length of the successive samples of the signal being processed (L).
    Overlap and save method is used since it requires no zero padding.
    '''

    def __init__(self, IR, length_of_input):
        # M = size of IR
        self.M = len(self.IR)
        # L = size of input samples to process
        self.L = length_of_input

        self.compute_IR(IR)

        self.output_fft = np.zeros(self.L + self.M - 1)
        self.output = np.zeros(self.L + self.M - 1)
        

    def compute_IR(self, IR):
        # Impulse Response with zero padding that will match the length of the input samples
        self.IR = IR
        # Transfer Function: DFT of the impulse response
        self.TF = np.fft.fft(self.IR, self.L + self.M - 1)


    def conv_cycle(self, input_signal, impulse_response):
        # Zero padding input so that the FFT matches the size of the TF being used.
        input_fft = np.fft.fft(input_signal)

        self.output_fft = np.multiply(input_fft, self.TF)
        self.output = np.fft.ifft(self.output_fft)
        return self.output