import numpy as np
import scorpy
import os
import h5py

import glob

import matplotlib.pyplot as plt
plt.close('all')


geom= '19MPz18'
size = '1000nm'


# print('making glob')
# aglob = glob.glob(f'/media/pat/datadrive/ice/sim/corr/{geom}/{size}-qmin15/hex-ice-{size}-qmin15-{geom}-*-1-sq.py')
# print('done')

# for i in aglob: 
    # print(i)

# print(len(aglob))


imax = 160
jmax = 10


xs = np.zeros( (imax, jmax ))

for i in range(1, imax+1):
    for j in range(1, jmax+1):
        print(i, j)
        corr_sq = scorpy.CorrelationVol(path=f'{scorpy.DATADIR}/ice/sim/corr/{geom}/{size}-qmin15/hex-ice-{size}-qmin15-{geom}-{i}-{j}-qcor-sq.npy')
        corr = scorpy.CorrelationVol(path=f'{scorpy.DATADIR}/ice/sim/corr/{geom}/{size}-qmin15/hex-ice-{size}-qmin15-{geom}-{i}-{j}-qcor.npy')



        corr_sq_mean = corr_sq.vol.mean()
        corr_mean_sq = corr.vol.mean()**2

        del corr_sq
        del corr


        x = np.sqrt(corr_sq_mean - corr_mean_sq)


        xs[i-1, j-1] = x




plt.show()
