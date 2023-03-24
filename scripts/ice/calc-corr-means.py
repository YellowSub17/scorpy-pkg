import numpy as np
import scorpy
import os
import sys
import h5py

import glob

import matplotlib.pyplot as plt
plt.close('all')


geom= '19MPz18'
# size = '1000nm'


size = sys.argv[1]


imax = 160
jmax = 250


corr_sq_means = np.zeros( (imax, jmax ))
corr_means = np.zeros( (imax, jmax ))

for i in range(1, imax+1):
    for j in range(1, jmax+1):
        print(i, j)
        corr_sq = scorpy.CorrelationVol(path=f'{scorpy.DATADIR}/ice/sim/corr/{geom}/{size}-qmin15/hex-ice-{size}-qmin15-{geom}-{i}-{j}-qcor-sq.npy')
        corr = scorpy.CorrelationVol(path=f'{scorpy.DATADIR}/ice/sim/corr/{geom}/{size}-qmin15/hex-ice-{size}-qmin15-{geom}-{i}-{j}-qcor.npy')


        corr_sq_means[i-1, j-1] = corr_sq.vol.mean()
        corr_means[i-1, j-1] = corr.vol.mean()


        del corr_sq
        del corr


        np.save(f'/media/pat/datadrive/ice/sim/corr/19MPz18/means/hex-ice-{size}-qmin15-{geom}-qcor-means.npy', corr_sq_means)
        np.save(f'/media/pat/datadrive/ice/sim/corr/19MPz18/means/hex-ice-{size}-qmin15-{geom}-qcor-sq-means.npy', corr_means)





plt.show()
