import numpy as np
import scorpy
import os
import h5py


import matplotlib.pyplot as plt
plt.close('all')





for i in range(1, 3721):
    print(i, end='\r')



    pk1 = scorpy.PeakData(datapath=f'{scorpy.DATADIR}/ice/sim/patterns/hex-ice-1um-{i}.npz',
                         geompath=f'{scorpy.DATADIR}/ice/sim/geoms/det-1MP-panel.geom')


    inte = pk1.integrate_peaks(0.005)
    pk1.calc_scat(inte[:,0:3], inte[:,-1])


    corr = scorpy.CorrelationVol(100, 180, 2.35, cos_sample=False)
    corr.fill_from_peakdata(pk1,verbose=0)
    corr.save(fpath=f'{scorpy.DATADIR}/ice/sim/corr/hex-ice-1um-{i}-qcor.npy')














