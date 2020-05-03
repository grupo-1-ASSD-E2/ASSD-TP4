import pyo

s = pyo.Server().boot()
s.start()
snd = 'C:/Users/facun/OneDrive/Desktop/ITBA/6C ASSD/ASSD-TP4/Resources/Audio files/Multitracks Bohemian Rhapsody/03 - Borap03.mp3'
sf = pyo.SfPlayer(snd, speed=[.999,1], loop=True, mul=.25).out()
a = pyo.Convolve(sf, pyo.SndTable(SNDS_PATH+'/accord.aif'), size=512, mul=.2).out()