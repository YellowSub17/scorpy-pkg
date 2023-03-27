import numpy as np
import scorpy
import os
import h5py


import matplotlib.pyplot as plt
plt.close('all')





cif = scorpy.CifData(path = '/media/pat/datadrive/ice/sim/struct/hex-ice-sf.cif', qmax=3.1)

corr = scorpy.CorrelationVol(nq=100, npsi=180, qmax=3.1, qmin=1.5, cos_sample=False)

corr.fill_from_cif(cif, verbose=99)


corr.save('/media/pat/datadrive/ice/sim/corr/hex-ice-qcor.npy')




