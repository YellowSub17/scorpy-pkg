import numpy as np
import scorpy
import os
import h5py

import glob

import matplotlib.pyplot as plt
plt.close('all')


geom= '19MPz18'
size = '1000nm'




pk = scorpy.PeakData(datapath=f'{scorpy.DATADIR}/ice/sim/patterns/{geom}/{size}/hex-ice-{size}-{geom}-{1}-{1}.npz',
                             geompath=f'{scorpy.DATADIR}/ice/sim/geoms/{geom}.geom')


pk.plot_peaks()
pk.plot_peakr(0.005)

inte = pk.integrate_peaks(0.005)
pk.calc_scat(inte[:,0:3], inte[:,-1])

pk.plot_peaks()

plt.show()


