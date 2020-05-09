from audio_processing.convolutioner import Convolutioner

br_tracks_paths = []
for i in range(1,25):
    br_tracks_paths.append('././Resources/Audio files/Multitracks Bohemian Rhapsody/{:02d} - Borap{:02d}.wav'.format(i, i))

conv = Convolutioner(input_files=br_tracks_paths)
conv.save_input_array('processing_api_3D/tests output/Bohemian Rhapsody ndarray.npy')