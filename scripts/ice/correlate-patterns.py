import numpy as np
import scorpy
import os
import h5py


import matplotlib.pyplot as plt
plt.close('all')





for chunk in range(10):
    print(chunk)
    for i in range(1, 1001):

        pk1 = scorpy.PeakData(datapath=f'{scorpy.DATADIR}/ice/sim/patterns/14MP/hex-ice-250nm-14MP-{chunk}-{i}.npz',
                             geompath=f'{scorpy.DATADIR}/ice/sim/geoms/14MP.geom')


        inte = pk1.integrate_peaks(0.005)
        pk1.calc_scat(inte[:,0:3], inte[:,-1])


        corr = scorpy.CorrelationVol(100, 180, 3.8, cos_sample=False)
        corr.fill_from_peakdata(pk1,verbose=0)
        corr.save(fpath=f'{scorpy.DATADIR}/ice/sim/corr/hex-ice-250nm-14MP-{chunk}-{i}-qcor.npy')














