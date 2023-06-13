

import scorpy
import numpy as np
import matplotlib.pyplot as plt
import os
import sys
import subprocess
import h5py
import scipy as sp
import time

# corr = scorpy.CorrelationVol(nq=256, npsi=360, qmax=1.5, qmin=0.2, cos_sample=False)
corr = scorpy.CorrelationVol(nq=256, npsi=360, qmax=1.5, qmin=0.4, cos_sample=False)



npz_fname =  f'/home/ec2-user/corr/data/frames/193l-500nm-19MPz40-test-2.npz'
pk = scorpy.PeakData(npz_fname, '/home/ec2-user/corr/data/geom/19MPz40.geom')



pk.plot_peaks()
pk.plot_peakr(0.005)

inte = pk.integrate_peaks(0.005)
pk.calc_scat(inte[:,0:3], inte[:,-1])

pk.plot_peaks()

pk.plot_qring(0.2)
pk.plot_qring(1.5)

corr.fill_from_peakdata(pk)


corr.plot_q1q2()
corr.plot_sumax(1)


corr.save(f'/home/ec2-user/corr/data/qcor/193l-500nm-19Mz40-test-2-qcor2.npy')
corr.save(f'/home/ec2-user/corr/data/qcor/193l-500nm-19Mz40-test-2-qcor2.dbin')
plt.show()





