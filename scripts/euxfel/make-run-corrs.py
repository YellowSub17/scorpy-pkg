#!/usr/bin/env python3
import scorpy
import numpy as np
import time

import os
import matplotlib.pyplot as plt




qmax = 1.45
wavelength = 1.333e-10
clen = 0.1697469375
res = 5000
nq =100
npsi = 180
method='scat_pol'
npeakmax = 150

r = scorpy.utils.convert_q2r(qmax, clen, wavelength*1e10)





runs = [108, 113, 109, 125, 110, 123, 118, 112,119,120,102,104,105,103,121,126]
runs = [123, 118, 112,119,120,102,104,105,103,121,126]





#### SCORPY CORRELATION
for run in runs:

    print(f'######Run {run}')
    pk = scorpy.PeakData(f'{scorpy.DATADIR}/cxi/run{run}_peaks.txt', qmax=qmax)

    corr = scorpy.CorrelationVol(nq=nq, npsi=npsi, qmax=qmax, cos_sample=False)
    corr.fill_from_peakdata(pk, npeakmax=npeakmax, method=method)
    corr.save(f'{scorpy.DATADIR}/dbins/cxi/qcors/{run}/run{run}-qcor.dbin')


    ### Seeded Half runs
    for seed in range(20):
        print(f'Run: {run}')
        print(f'Seed: {seed}.')
        frames = pk.split_frames()
        np.random.seed(seed)
        np.random.shuffle(frames)

        frames_a = frames[:int(len(frames)/2)]
        frames_b = frames[int(len(frames)/2):]


        corra = scorpy.CorrelationVol(nq, npsi, qmax, cos_sample=False)
        for i, frame in enumerate(frames_a):
            print(f'\x1b[2Ka Frame {i}', end='\r')
            corra.fill_from_peakdata(frame, method=method, npeakmax=npeakmax)
        corra.save(f'../../data/dbins/cxi/qcors/{run}/run{run}-seed{seed}a-qcor.dbin')

        corrb = scorpy.CorrelationVol(nq, npsi, qmax, cos_sample=False)
        for i, frame in enumerate(frames_b):
            print(f'\x1b[2Kb Frame {i}', end='\r')
            corrb.fill_from_peakdata(frame, method=method, npeakmax=npeakmax)
        corrb.save(f'../../data/dbins/cxi/qcors/{run}/run{run}-seed{seed}b-qcor.dbin')
        print()










