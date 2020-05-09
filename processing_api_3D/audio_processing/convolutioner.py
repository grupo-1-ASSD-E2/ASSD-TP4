import numpy as np
import scipy.signal as ss
import scipy.io.wavfile as sw
import pyaudio
import librosa
import wave


np_to_pa_format = {
    np.dtype('float32') : pyaudio.paFloat32,
    np.dtype('int32') : pyaudio.paInt32,
    np.dtype('int16') : pyaudio.paInt16,
    np.dtype('int8') : pyaudio.paInt8,
    np.dtype('uint8') : pyaudio.paUInt8
}
np_type_to_sample_width = {
    np.dtype('float32') : 4,
    np.dtype('int32') : 4,
    np.dtype('int16') : 3,
    np.dtype('int8') : 1,
    np.dtype('uint8') : 1
}

STEREO = 2


class Convolutioner:
    '''
    Provides methods for DSP in real time.
    Minimum requirements for working are a given impulse response (IR), and the length of the successive samples of the signal being processed (L).
    Overlap and save method is used since it requires no zero padding.

    input_files is a list of files containing paths to files containing the tracks to be processed. self.input_array will be a numpy array constructed from the data in those files.
    Formats like mp3 or wav are accepted.

    input_rate is the sampling rate in Hz used for sampling the audio input file. Default is 44.1KHz.

    input_dtype is the data type used for each element in self.input_array. Default is np.float32. 
    np.float64 and np.int64 will be casted to np.float32 and np.int32 since float64 and int64 are not supported by PyAudio.

    frame_count is the amount of samples to be processed in call of the callback. Default is 2**15.

    The method that processes the frames can me changed. Default is processing using the IRs.
    To change it call:
        self.custom_processing_callback(my_callback)
    my_callback should receive one argument 'audio_frame' of shape (self.tracks_num, self.frame_count) and return a tuple (audio_left_processed, audio_right_processed)
    
    IR_left, IR_right are the impulse response of the filter which will be used to process left and right channels, respectively. Must be array-like (1D or 2D). 
    If both are the same, the sound will be same as mono, if different, stereo.
    If IR_left and IR_right are 1D, it will be assumed that all tracks in input_array are to be processed by the same IR_left and IR_right.
    If IR_left and IR_right are 2D and have the same amount of rows as input_array, it means that not all the IRs should be the same, and therefore each track will be processed by the corresponding IR of the same row.
    If IR_left and IR_right are 2D but have a smaller amount of rows than the input_array, the remaining rows will be assumed to be a delta (and as such, the track will exit as it entered).
    If IR_left and IR_right are 2D but have a larger amount of rows from input_array, the exceeding rows will be ignored.
    '''

    def __init__(self, IR_left=np.ones(1), IR_right=np.ones(1), input_files=[], input_rate=44100, input_dtype=np.float32, frame_count=2**15):
        # Amount of samples to be processed in call of the callback.
        self.frame_count=frame_count
        self.compute_input_files(input_files, input_rate, input_dtype)
        self.compute_IR(IR_left, IR_right)

        # Keeps count of the frames processed by the callback in non blocking mode.
        self.cycle_count = 0
        # Output data as an ndarray, where each row is a track in the song/sound.
        self.output_array = np.array([[], []], dtype=self.input_array.dtype).T
        # If True, output is saved to self.output_array.
        self.save_output = True
        # Determines gain of added tracks when mixing them (generally <1).
        self.auto_adjust_mixing_gain()

        # When working with non blocking mode, this saves the last elements of the previos frame processed to add them to the first elements of the new frame processed (overlap and add)
        self.leftover_left = np.zeros((self.tracks_num, self.frame_count + self.M_left - 1), dtype=self.input_array.dtype)
        self.leftover_right = np.zeros((self.tracks_num, self.frame_count + self.M_right - 1), dtype=self.input_array.dtype)

        # Method that processes the frames. Default is processing using the IRs, but can be changed
        self.processing_callback = self.convolve_cycle


    def compute_input_files(self, files, input_rate=44100, input_dtype=np.float32):
        # Sampling rate of the audio files.
        self.sample_rate = int(input_rate)

        audio_data = []
        for file_path in files:
            new_data, new_rate = librosa.load(file_path, sr=self.sample_rate, dtype=input_dtype)
            audio_data.append(new_data.tolist())

        # Adding zeros to make all files of the same size.
        try:
            max_size_file = max([len(track) for track in audio_data])
            for i in range(len(audio_data)):
                audio_data[i] = audio_data[i] + [0] * (max_size_file - len(audio_data[i]))

        except ValueError:
            pass

        self.set_input(audio_data, tracks_dtype=input_dtype)


    def set_input(self, tracks, tracks_dtype):
        '''
        tracks_to_add must be an ndarray containint the tracks as rows.
        '''
        # Input data to process as an ndarray, where each row is a track in the song/sound.
        self.input_array = np.array(tracks, dtype=tracks_dtype)
        if self.input_array.ndim == 1:
            self.input_array = np.reshape(self.input_array, (1, len(tracks)))
            
        self.adjust_to_new_input()


    def update_input(self, tracks, tracks_dtype):
        '''
        tracks_to_add must be an ndarray containint the tracks as rows.
        Difference with set_input is that this method can only be called after __init__ is called and it will adjust the IRs and leftovers to the new input.
        '''
        # Input data to process as an ndarray, where each row is a track in the song/sound.
        self.input_array = np.array(tracks, dtype=tracks_dtype)
        if self.input_array.ndim == 1:
            self.input_array = np.reshape(self.input_array, (1, len(tracks)))
            
        self.adjust_to_new_input()
        self.compute_IR(self.IR_left, self.IR_right)
        self.leftover_left = np.zeros((self.tracks_num, self.frame_count + self.M_left - 1), dtype=self.input_array.dtype)
        self.leftover_right = np.zeros((self.tracks_num, self.frame_count + self.M_right - 1), dtype=self.input_array.dtype)


    def add_tracks_to_input(self, tracks_to_add):
        '''
        tracks_to_add must be an ndarray containint the tracks as rows.
        '''
        self.input_array = np.vstack(self.input_array, tracks_to_add, dtype=self.input_array.dtype)
        self.adjust_to_new_input()


    def adjust_to_new_input(self):
        '''
        Adjusts class variables to new input.
        '''
        # Number of tracks, a.k.a. number of rows in self.input_array.
        self.tracks_num = self.input_array.shape[0]
        # Number of tracks to process, i.e. number of row in self.input_array.
        self.L = self.input_array.shape[1]
        

    def compute_IR(self, IR_left, IR_right):
        # Impulse Response for the left channel
        self.IR_left = np.array(IR_left, dtype=self.input_array.dtype)
        self.IR_left = self.reshape_IR(self.IR_left)

        # Impulse Response for the right channel
        self.IR_right = np.array(IR_right, dtype=self.input_array.dtype)
        self.IR_right = self.reshape_IR(self.IR_right)

        # M = size of IR_left.
        self.M_left = self.IR_left.shape[1]
        # M = size of IR_right.
        self.M_right = self.IR_right.shape[1]


    def reshape_IR(self, IR):
        if IR.ndim == 1:
            # If it's 1D, it gets reshaped to match this class methods syntax.
            IR_ret = np.array([np.zeros(IR.size)], dtype=self.input_array.dtype)
            IR_ret[0] = IR
            # Repeating IR for every track.
            for i in range(self.input_array.shape[0] - 1):
                IR_ret = np.vstack((IR_ret, IR))

        elif IR.shape[0] < self.input_array.shape[0]:
            # Filling the IR with deltas
            IR_ret = IR
            deltas_to_add = self.input_array.shape[0] - IR.shape[0]
            IR_delta = np.hstack((1 * np.ones((deltas_to_add, 1), dtype=self.input_array.dtype), np.zeros((deltas_to_add, IR.shape[1] - 1), dtype=self.input_array.dtype)))
            IR_ret = np.vstack((IR_ret, IR_delta))

        else:
            IR_ret = IR

        return IR_ret


    def auto_adjust_mixing_gain(self):
        '''
        Determines optimum gain to apply to the mixing of tracks.
        '''
        #TODO MAKE THIS PROPERLY: THis is hardcoded for HUTUBS HRIRs.
        self.mixing_gain = 2**(-3)


    def set_mixing_gain(self, gain):
        self.mixing_gain = gain


    def custom_processing_callback(self, custom_callback):
        self.processing_callback = custom_callback


    def start_non_blocking_processing(self, save_output=True, frame_count=2**15, listen_output=True):
        '''
        Non blocking mode works on a different thread, therefore, the main thread must be kept active with, for example:
            while processing():
                time.sleep(1)
        '''
        self.save_output = save_output
        self.frame_count = frame_count

        # Initiate PyAudio
        self.pa = pyaudio.PyAudio()
        # Open stream using callback
        self.stream = self.pa.open(format=np_to_pa_format[self.input_array.dtype],
                        channels=STEREO,
                        rate=self.sample_rate,
                        output=listen_output,
                        input=not listen_output,
                        stream_callback=self.pyaudio_callback,
                        frames_per_buffer=frame_count)

        # Start the stream
        self.stream.start_stream()


    def processing(self):
        '''
        Returns true if the PyAudio stream is still active in non blocking mode.
        MUST be called AFTER self.start_non_blocking_processing.
        '''
        return self.stream.is_active()


    def terminate_processing(self):
        '''
        Terminates stream opened by self.start_non_blocking_processing.
        MUST be called AFTER self.processing returns False.
        '''
        # Stop stream
        self.stream.stop_stream()
        self.stream.close()

        # Close PyAudio
        self.pa.terminate()


    def start_blocking_processing(self):
        # Setting up output arrays.
        audio_left = np.zeros((self.tracks_num, self.L + self.M_left - 1), dtype=self.input_array.dtype)
        audio_right = np.zeros((self.tracks_num, self.L + self.M_right - 1), dtype=self.input_array.dtype)

        # Processing each track of the frame using the scipy overlap and add convolution, but also performing overlap and on the whole thing since we are processing the input by frames.
        for i in range(self.input_array.shape[0]):
            audio_left[i]  = ss.oaconvolve(self.input_array[i], self.IR_left[i], mode='full')
            audio_right[i] = ss.oaconvolve(self.input_array[i], self.IR_right[i], mode='full')
    
        # Saving last self.M - 1 elements for next cycle.
        self.leftover_left = np.hstack((audio_left[:, self.L:], np.zeros((self.tracks_num, self.L), dtype=self.input_array.dtype)))
        self.leftover_right = np.hstack((audio_right[:, self.L:], np.zeros((self.tracks_num, self.L), dtype=self.input_array.dtype)))

        # Discarding last self.M - 1 elements.
        audio_left = audio_left[:, :self.L]
        audio_right = audio_right[:, :self.L]

        # Mixing tracks.
        audio_left = self.mixing_gain * np.sum(audio_left, axis=0)
        audio_right = self.mixing_gain * np.sum(audio_right, axis=0)
    
        # Preparing data to send to PyAudio.
        out_data = np.empty((audio_left.size + audio_right.size), dtype=self.input_array.dtype)
        # Odd elements are going to the left channel.
        out_data[1::2] = audio_left
        # Even elements are going to the right channel.
        out_data[0::2] = audio_right

        if self.save_output:
            self.output_array = np.hstack((audio_left, audio_right))


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

        audio_left, audio_right = self.processing_callback(audio_frame)

        # Mixing tracks.
        audio_left = self.mixing_gain * np.sum(audio_left, axis=0)
        audio_right = self.mixing_gain * np.sum(audio_right, axis=0)
    
        # Preparing data to send to PyAudio.
        out_data = np.empty((audio_left.size + audio_right.size), dtype=self.input_array.dtype)
        # Odd elements are going to the left channel.
        out_data[1::2] = audio_left
        # Even elements are going to the right channel.
        out_data[0::2] = audio_right

        if self.save_output:
            self.output_array = np.vstack((self.output_array, np.vstack((audio_left, audio_right)).T))
        
        ret_data = out_data.tostring()

        self.cycle_count += 1
        
        return (ret_data, pyaudio.paContinue)


    def convolve_cycle(self, audio_frame):
        '''
        Processing each track of the frame using the scipy overlap and add convolution, but also performing overlap and on the whole 
        thing since we are processing the input by frames.
        '''
        # Setting up output arrays.
        audio_left = np.zeros((self.tracks_num, self.frame_count + self.M_left - 1), dtype=self.input_array.dtype)
        audio_right = np.zeros((self.tracks_num, self.frame_count + self.M_right - 1), dtype=self.input_array.dtype)

        for i in range(audio_frame.shape[0]):
            try:
                audio_left[i] = ss.oaconvolve(audio_frame[i], self.IR_left[i], mode='full') + self.leftover_left[i]
                audio_right[i] = ss.oaconvolve(audio_frame[i], self.IR_right[i], mode='full') + self.leftover_right[i]
            except ValueError:
                print(audio_frame[i].shape)
                print(self.IR_left[i].shape)
    
        # Saving last self.M - 1 elements for next cycle.
        self.leftover_left = np.hstack((audio_left[:, self.frame_count:], np.zeros((self.tracks_num, self.frame_count), dtype=self.input_array.dtype)))
        self.leftover_right = np.hstack((audio_right[:, self.frame_count:], np.zeros((self.tracks_num, self.frame_count), dtype=self.input_array.dtype)))

        # Discarding last self.M - 1 elements.
        audio_left = audio_left[:, :self.frame_count]
        audio_right = audio_right[:, :self.frame_count]

        return (audio_left, audio_right)


    def get_output_file(self, path_to_output, sample_rate=None):
        if sample_rate == None:
            sample_rate = self.sample_rate

        sw.write(path_to_output, sample_rate, self.output_array)


    def save_input_array(self, path_to_input_array):
        np.save(path_to_input_array, self.input_array)


    def save_output_array(self, path_to_input_array):
        np.save(path_to_input_array, self.output_array)