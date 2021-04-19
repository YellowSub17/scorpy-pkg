#!/usr/bin/env python3
'''
make-corr.py

Make correlation vol objects.
'''

import scorpy
import numpy as np
np.random.seed(0)




#### MAKE CORRELATION FROM CIF DATA
names  =['1al1'] # 1al1 qmax 0.36992983463258367
nq = 200
ntheta = 360



for name in names:
    print(f'Correlating: {name}')
    cif = scorpy.CifData(f'../data/xtal/{name}-sf.cif')

    cor = scorpy.CorrelationVol(nq, ntheta, cif.qmax)

    cor.correlate(cif.scattering)
    # print(f'\nDone.')
    cor.save_dbin(f'../data/dbins/{name}_qcor')





#### MAKE CORRELATION FROM PEAK DATA

runs150 = [112,123,113,125,102,103,104,105]
runs144 = [118,108,119,109,120,110,121]
runs = runs150+runs144


nseeds = 20
nq = 100
ntheta = 180
qmax = 1.4
npeaksmax = 150

geo = scorpy.ExpGeom('../data/geoms/agipd_2304_vj_opt_v3.geom')

for run in runs:

    print(f'Correlating run: {run}')
    peaks = scorpy.PeakData(f'../data/cxi/{run}/peaks.txt', geo)
    frames = [i for i in peaks.split_frames() if i.qlist.shape[0]<npeaksmax]
    half_ind = int(len(frames)/2)



    corr = scorpy.CorrelationVol(nq,ntheta, qmax)
    for frame in frames:
        corr.correlate(frame.qlist[:,-3:])
    corr.save_dbin(f'../data/dbins/cosine_sim/{run}/run{run}_qcor')


    for seed in range(nseeds):
        print(f'Correlating seed: {seed}')

        seed_frames = list(frames)
        np.random.shuffle(seed_frames)

        corra_frames = seed_frames[:half_ind]
        corrb_frames = seed_frames[half_ind:]

        corra = scorpy.CorrelationVol(nq,ntheta,qmax)
        for frame in corra_frames:
            corra.correlate(frame.qlist[:,-3:])
        corra.save_dbin(f'../data/dbins/cosine_sim/{run}/run{run}_seed{seed}a_qcor')

        corrb = scorpy.CorrelationVol(nq,ntheta,qmax)
        for frame in corrb_frames:
            corrb.correlate(frame.qlist[:,-3:])
        corrb.save_dbin(f'../data/dbins/cosine_sim/{run}/run{run}_seed{seed}b_qcor')


