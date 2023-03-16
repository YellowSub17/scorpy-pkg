import numpy as np
import scorpy
import os
import h5py


import matplotlib.pyplot as plt
plt.close('all')





cif = scorpy.CifData(path = '/media/pat/datadrive/ice/sim/struct/hex-ice-sf.cif', qmax=3.1)

corr = scorpy.CorrelationVol(100, 180, 3.1, cos_sample=False)

corr.fill_from_cif(cif, verbose=99)


corr.save('/media/pat/datadrive/ice/sim/corr/hex-ice-qcor.npy')




