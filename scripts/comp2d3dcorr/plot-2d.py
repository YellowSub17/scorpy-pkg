import numpy as np
import h5py

import scorpy

import matplotlib.pyplot as plt
plt.close('all')







geo = scorpy.ExpGeom(f'{scorpy.DATADIR}/geoms/single_square.geom')
# pk = scorpy.PeakData(f'{scorpy.DATADIR}/cxi/run118_peaks.txt')
pk = scorpy.PeakData(f'{scorpy.DATADIR}/patternsim/plot-test.h5', geo=geo, qmax=1, qmin=0.01)
pk.plot_peaks()
pk.geo.plot_qring(q=0.54)
pk.geo.plot_qring(q=0.6)

corr1 = scorpy.CorrelationVol(nq=100, npsi=180, qmax=pk.qmax, cos_sample=False, inc_self_corr=False)

corr1.save('/tmp/x.dbin')

corr2 = scorpy.CorrelationVol(path='/tmp/x.dbin')
# print(corr2.cos_sample)



# corr2.fill_from_peakdata(pk, verbose=99)
# corr2.plot_sumax(0)
# corr2.plot_q1q2()







# geo = scorpy.ExpGeom(f'{scorpy.DATADIR}/geoms/single_square.geom')
# pk = scorpy.PeakData(f'{scorpy.DATADIR}/patternsim/plot-test.h5', geo=geo, qmin=0.01 )



# pk.plot_peaks()

# qs = [0.01, 0.25, 0.5, 0.75, 1]#, 1.25, 1.5, 1.75, 2]
# for q in qs:
    # pk.geo.plot_qring(q=q)



# corr = scorpy.CorrelationVol(path=f'{scorpy.DATADIR}/dbins/1vds-2d-10kframes-qcor.dbin')
# corr.plot_q1q2()






plt.show()

