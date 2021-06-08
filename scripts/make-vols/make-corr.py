#!/usr/bin/env python3
'''
make-corr.py

Make correlation vol objects.
'''

import matplotlib.pyplot as plt
import scorpy
from scorpy import __DATADIR
import numpy as np
import time
np.random.seed(0)


####### MAKE CORRELATION FROM CIF DATA

names = ['1vds_fj',] # 1al1 qmax 0.36992983463258367
nq = 100
ntheta = 180
qmax = 1.4



for name in names:
    print(f'Correlating: {name}')
    cif = scorpy.CifData(f'{__DATADIR}/xtal/{name}-sf.cif')
    print(cif.scat_sph.shape)
    corr = scorpy.CorrelationVol(nq, ntheta, qmax)
    corr.fill_from_cif(cif)
    corr.save(f'{__DATADIR}/dbins/{name}_qcor')


# ######## MAKE CORRELATION FROM ENSEMBLE PEAKS

# ns = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024]

# nq = 100
# npsi = 180
# nseeds = 10

# geo = scorpy.ExpGeom('../data/geoms/agipd_2304_vj_opt_v3.geom')

# for seed in range(nseeds):
    # print(time.asctime())
    # for n in ns:
        # print('n:', n, 'seed:', seed)

        # pk = scorpy.PeakData(
            # f'../data/ensemble_peaks/n{n}/peaks_{n}_{seed}.txt', geo, cxi_flag=False)

        # corr = scorpy.CorrelationVol(nq, npsi, qmax=1.4)

        # corr.fill_from_peakdata(pk)

        # corr.save(f'../data/dbins/ensemble_peaks/ensemble_n{n}_{seed}')


######## MAKE CORRELATION FROM PEAK DATA

# runs150 = [112,123,113,125,102,103,104,105]
# runs144 = [118,108,119,109,120,110,121]
# runs = runs150+runs144


# nseeds = 20
# nq = 200
# ntheta = 360
# qmax = 1.4
# npeaksmax = 150

# geo = scorpy.ExpGeom('../data/geoms/agipd_2304_vj_opt_v3.geom')

# for run in runs:

    # print(f'Correlating run: {run}')
    # peaks = scorpy.PeakData(f'../data/cxi/{run}/peaks.txt', geo)
    # frames = [i for i in peaks.split_frames() if i.scat_pol.shape[0]<npeaksmax]
    # half_ind = int(len(frames)/2)

    # corr = scorpy.CorrelationVol(nq,ntheta, qmax)
    # for frame in frames:
    # corr.fill_from_peakdata(frame)
    # corr.save(f'../data/dbins/cosine_sim/{run}/run{run}_qcor')


# # #     for seed in range(nseeds):
    # # # print(f'Correlating seed: {seed}')

    # # # seed_frames = list(frames)
    # # # np.random.shuffle(seed_frames)

    # # # corra_frames = seed_frames[:half_ind]
    # # # corrb_frames = seed_frames[half_ind:]

    # # # corra = scorpy.CorrelationVol(nq,ntheta,qmax)
    # # # for frame in corra_frames:
    # # # corra.fill_from_peakdata(frame)
    # # # corra.save_dbin(f'../data/dbins/cosine_sim/{run}/run{run}_seed{seed}a_qcor')

    # # # corrb = scorpy.CorrelationVol(nq,ntheta,qmax)
    # # # for frame in corrb_frames:
    # # # corrb.fill_from_peakdata(frame)
    # # # corrb.save_dbin(f'../data/dbins/cosine_sim/{run}/run{run}_seed{seed}b_qcor')
