

import scorpy
import matplotlib.pyplot as plt





cif = scorpy.CifData('../data/xtal/1al1-sf.cif')

qti = cif.scattering[::100,:]
correl = scorpy.CorrelationVol(100,180,cif.qmax)
correl.correlate(qti)

correl.plot_q1q2()
correl.plot_sumax(axis=1)

plt.show()
