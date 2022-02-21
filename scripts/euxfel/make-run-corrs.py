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



runs = [108, 109, 110, 113, 118, 123, 125]





#### SCORPY CORRELATION
for run in runs:

    print(f'####### Run {run}')
    pk = scorpy.PeakData(f'{scorpy.DATADIR}/cxi/run{run}_peaks.txt', qmax=qmax)

    corr = scorpy.CorrelationVol(nq=nq, npsi=npsi, qmax=qmax, cos_sample=False)
    corr.fill_from_peakdata(pk, npeakmax=npeakmax, method=method)
    corr.save(f'../../data/dbins/cxi/run{run}-qcor.dbin')


    ### Seeded Half runs
    for seed in range(20):
        print(seed)
        frames = pk.split_frames(npeakmax=150)
        np.random.seed(seed)
        np.random.shuffle(frames)

        frames_a = frames[:int(len(frames)/2)]
        frames_b = frames[int(len(frames)/2):]


        corra = scorpy.CorrelationVol(nq, npsi, qmax, cos_sample=False)
        for i, frame in enumerate(frames_a):
            print(f'a Frame {i}', end='\r')
            corra.fill_from_peakdata(frame, method=method, npeakmax=npeakmax)
        corra.save(f'../../data/dbins/cxi/seeds/run{run}-seed{seed}a-qcor.dbin')

        corrb = scorpy.CorrelationVol(nq, npsi, qmax, cos_sample=False)
        for i, frame in enumerate(frames_b):
            print(f'b Frame {i}', end='\r')
            corrb.fill_from_peakdata(frame, method=method, npeakmax=npeakmax)
        corrb.save(f'../../data/dbins/cxi/seeds/run{run}-seed{seed}b-qcor.dbin')








##### PADFCORR CORRELATION


# for run in runs:
    # print(f'####### Run {run}')

    # pk = scorpy.PeakData(f'{scorpy.DATADIR}/cxi/run{run}_peaks.txt', qmax=qmax)

    # run_corr = scorpy.CorrelationVol(nq, npsi, qmax, cos_sample=False)

    # frames = pk.split_frames(npeakmax=150)
    # nframes = len(frames)

    # print('')
    # print('############')
    # print(f'Filling CorrelationVol from Peakdata via PADFCORR.')
    # print(f'Correlating {nframes} frames.')
    # print(f'Correlation started: {time.asctime()}\n')

    # for frame_i, frame_pk in enumerate(frames):

        # print(f'Frame: {frame_i+1}/{nframes}', end='\r')


        # im = frame_pk.make_im(r=r, fname=f'/tmp/tmp_frame_im.dbin')


        # corr_config = open(f'/tmp/padfcorr_tmp_config.txt', 'w')
        # corr_config.write(f'input = /tmp/tmp_frame_im.dbin\n')
        # corr_config.write(f'outpath = /tmp\n')
        # corr_config.write(f'wavelength = {wavelength}\n')
        # corr_config.write(f'pixel_width = {1/res}\n')
        # corr_config.write(f'detector_z = {clen}\n')
        # corr_config.write(f'nq = {nq}\n')
        # corr_config.write(f'nth = {npsi*2}\n')
        # corr_config.write(f'tag = padfcorr_tmp_frame\n')
        # corr_config.write(f'qmax = {qmax*1e9}\n')
        # corr_config.close()

        # os.system(f'{scorpy.PADFCORRDIR}padfcorr /tmp/padfcorr_tmp_config.txt')

        # tmppadfcorrvol = np.fromfile(f'/tmp/padfcorr_tmp_frame_correlation.dbin')
        # tmppadfcorrvol = tmppadfcorrvol.reshape((nq, nq, 2*npsi))

        # run_corr.vol += tmppadfcorrvol[:,:, :npsi]

        # # run_corr.save(f'{scorpy.DATADIR}/dbins/cxi/run{run}_padfcorr_qcor.dbin')

        # print('', end='')
    # print(f'Correlation finished: {time.asctime()}')
    # print('############')





plt.show()



