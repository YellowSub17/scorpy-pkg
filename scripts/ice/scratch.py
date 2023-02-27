import numpy as np
import scorpy
import os
import h5py


import matplotlib.pyplot as plt
plt.close('all')





corra = scorpy.CorrelationVol(100, 180, 2.35, cos_sample=False)
corrb = scorpy.CorrelationVol(100, 180, 2.35, cos_sample=False)


for i in range(1, 3721):
    print(i)
    corr = scorpy.CorrelationVol(path=f'{scorpy.DATADIR}/ice/sim/corr/hex-ice-1um-{i}-qcor.npy')
    if i%2==0:
        corra.vol +=corr.vol
    else:
        corrb.vol +=corr.vol





corra.plot_q1q2()
corrb.plot_q1q2()
plt.show()






