#!/usr/bin/env python3
'''
make-espk-corr.py

Make correlation vol objects from ensemble peak data.
'''

import matplotlib.pyplot as plt
import scorpy
from scorpy import __DATADIR
import numpy as np
import time
np.random.seed(0)



######## MAKE CORRELATION FROM ENSEMBLE PEAKS

ns = [1024]

nq = 100
npsi = 180

geo = scorpy.ExpGeom(f'{__DATADIR}/geoms/agipd_2304_vj_opt_v3.geom')

for seed in range(10, 30):
    print(time.asctime())
    for n in ns:
        print('n:', n, 'seed:', seed)

        pk = scorpy.PeakData(
            f'{__DATADIR}/ensemble_peaks/n{n}/peaks_{n}_{seed}.txt', geo, cxi_flag=False)

        corr = scorpy.CorrelationVol(nq, npsi, qmax=1.4)
        corr.fill_from_peakdata(pk)
        corr.save(f'{__DATADIR}/dbins/ensemble_peaks/ensemble_n{n}_{seed}')

print(time.asctime())








# plt.figure()
# ns = [1,2,4,6,16,32]
# times = [0.64, 1.43, 3.83, 7.412, 15.692, 30.35]
# plt.plot(ns, times)

# m = (times[-1] - times[-2]) / (ns[-1] - ns[-2])

# x = 1024
# y = m*x
# print(y)

# plt.plot(x, y, 'x')

# plt.show()
