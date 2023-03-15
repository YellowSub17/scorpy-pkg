import numpy as np
import scorpy
import os
import h5py


import matplotlib.pyplot as plt
plt.close('all')


geom =  '19MPz18'



for chunk in range(1, 81):
    print(chunk)
    for i in range(1, 251):

        pk1 = scorpy.PeakData(datapath=f'{scorpy.DATADIR}/ice/sim/patterns/{geom}/hex-ice-1000nm-{geom}-{chunk}-{i}.npz',
                             geompath=f'{scorpy.DATADIR}/ice/sim/geoms/{geom}.geom')


        inte = pk1.integrate_peaks(0.005)
        pk1.calc_scat(inte[:,0:3], inte[:,-1])


        corr = scorpy.CorrelationVol(100, 180, 3.1, cos_sample=False)
        corr.fill_from_peakdata(pk1,verbose=0)
        corr.save(fpath=f'{scorpy.DATADIR}/ice/sim/corr/{geom}/hex-ice-1000nm-{geom}-{chunk}-{i}-qcor.npy')














