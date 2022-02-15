import numpy as np
import h5py

import scorpy

import matplotlib.pyplot as plt
plt.close('all')















geo = scorpy.ExpGeom(f'{scorpy.DATADIR}/geoms/single_square.geom')

pk = scorpy.PeakData(f'{scorpy.DATADIR}/patternsim/1vds.h5', geo=geo, qmax=4.9, qmin=0.01)
pk.plot_peaks()
pk.geo.plot_qring(q=4.9)



corr = scorpy.CorrelationVol(nq=100, npsi=180, cos_sample=False, inc_self_corr=False, qmax=pk.qmax)
corr.fill_from_peakdata(pk, verbose=2, method='scat_pol')
corr.save(f'{scorpy.DATADIR}/dbins/1vds-2d.dbin')





corr.plot_q1q2()










plt.show()

