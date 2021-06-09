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

ns = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024]

nq = 100
npsi = 180
nseeds = 10

geo = scorpy.ExpGeom(f'{__DATADIR}/geoms/agipd_2304_vj_opt_v3.geom')

for seed in range(nseeds):
    print(time.asctime())
    for n in ns:
        print('n:', n, 'seed:', seed)

        pk = scorpy.PeakData(
            f'{__DATADIR}/ensemble_peaks/n{n}/peaks_{n}_{seed}.txt', geo, cxi_flag=False)

        corr = scorpy.CorrelationVol(nq, npsi, qmax=1.4)

        corr.fill_from_peakdata(pk)

        corr.save(f'{__DATADIR}/dbins/ensemble_peaks/ensemble_n{n}_{seed}')
