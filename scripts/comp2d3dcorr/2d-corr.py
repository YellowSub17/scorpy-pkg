import numpy as np
import h5py

import scorpy

import matplotlib.pyplot as plt
plt.close('all')













geo = scorpy.ExpGeom(f'{scorpy.DATADIR}/geoms/single_square.geom')
corr = scorpy.CorrelationVol(qmax=1, cos_sample=False, inc_self_corr=True)

for i in range(1, 1001):
    pk = scorpy.PeakData(f'{scorpy.DATADIR}/patternsim/1vds/1vds-{i}.h5', geo=geo, qmax=1, qmin=0.01)


    print(i, end='\r')

    corr.fill_from_peakdata(pk, verbose=0)

pk.plot_peaks()

corr.vol[0,:,:]=0
corr.vol[:,0,:]=0


fig, axes = plt.subplots(2,2)
plt.title('corr')
corr.plot_sumax(0, log=False, title='Sum through q1', fig=fig, axes=axes[0,0])
corr.plot_sumax(0, log=True, title='Sum through q1 (log)', fig=fig, axes=axes[0,1])

corr.plot_q1q2(log=False, title='q1q2', fig=fig, axes=axes[1,0])
corr.plot_q1q2(log=True, title='q1q2 (log)', fig=fig, axes=axes[1,1])


corr.save(f'{scorpy.DATADIR}/dbins/1vds-2d-qcor.dbin')









plt.show()

