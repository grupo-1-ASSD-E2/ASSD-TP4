from pyo import *

# duplex=1 to tell the Server we need both input and output sounds.
s = Server(duplex=1).boot()

# Length of the impulse response in samples.
TLEN = 512

# Conversion to seconds for NewTable objects.
DUR = sampsToSec(TLEN)

# Excitation signal for the filters.
sf = Noise(.5)

# Signal from the mic to record the kernels.
inmic = Input()

# Four tables and recorders.
t1 = NewTable(length=DUR, chnls=1)
r1 = TableRec(inmic, table=t1, fadetime=.001)

t2 = NewTable(length=DUR, chnls=1)
r2 = TableRec(inmic, table=t2, fadetime=.001)

t3 = NewTable(length=DUR, chnls=1)
r3 = TableRec(inmic, table=t3, fadetime=.001)

t4 = NewTable(length=DUR, chnls=1)
r4 = TableRec(inmic, table=t4, fadetime=.001)

# Interpolation control between the tables.
pha = Sig(0)
pha.ctrl(title="Impulse responses morphing")

# Morphing between the four impulse responses.
res = NewTable(length=DUR, chnls=1)
morp = TableMorph(pha, res, [t1,t2,t3,t4])

# Circular convolution between the excitation and the morphed kernel.
a = Convolve(sf, table=res, size=res.getSize(), mul=.1).mix(2).out()

s.gui(locals())