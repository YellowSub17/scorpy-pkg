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


# # MAKE CORRELATION FROM ENSEMBLE PEAKS

# ns = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024]
# nseeds = 10

# nq = 100
# npsi = 180
# qmax=1.4

# geo = scorpy.ExpGeom(f'{__DATADIR}/geoms/agipd_2304_vj_opt_v3.geom')

# for seed in range(nseeds):
    # for n in ns:
        # print()
        # print(f'Correlating Ensemble Peaks: n={n}, seed={seed}')

        # pk = scorpy.PeakData(
            # f'{__DATADIR}/espk/n{n}/peaks_{n}_{seed}.txt', geo, cxi_flag=False, qmax=qmax)

        # corr = scorpy.CorrelationVol(nq, npsi, qmax=qmax)
        # corr.fill_from_peakdata(pk, method='scat_pol')
        # corr.save(f'{__DATADIR}/dbins/espk/ensemble_n{n}_{seed}')
        # print()
        # print()

# MAKE CORRELATION FROM ENSEMBLE PEAKS


nq = 100
npsi = 180
qmax=3.5

geo = scorpy.ExpGeom(f'{__DATADIR}/geoms/agipd_2304_vj_opt_v3.geom')

for n in range(1,65):
    print()
    print(f'Correlating test Peaks: n={n}')

    pk = scorpy.PeakData(
        f'{__DATADIR}/test/test-{n}.txt', geo, cxi_flag=False, qmax=3.5)

    corr = scorpy.CorrelationVol(nq, npsi, qmax=pk.qmax)
    corr.fill_from_peakdata(pk, method='scat_pol')
    corr.save(f'{__DATADIR}/test/test-{n}_qcor')
    print()
    print()





