
import scorpy
import numpy as np
import time

import os
import matplotlib.pyplot as plt




qmax = 1.8
wavelength = 1.333e-10
clen = 0.1697469375
res = 5000
nq = 100
npsi = 180

r = scorpy.utils.convert_q2r(qmax, clen, wavelength*1e10)



# runs = [108, 109, 110, 113, 118, 123, 125]

runs = [118]




# #### SCORPY CORRELATION
# for run in runs:

    # print(f'####### Run {run}')
    # pk = scorpy.PeakData(f'{scorpy.DATADIR}/cxi/run{run}_peaks.txt', qmax=qmax)

    # corr = scorpy.CorrelationVol(nq=nq, npsi=npsi, qmax=qmax, cos_sample=False)
    # corr.fill_from_peakdata(pk, npeakmax=150, method='scat_pol')
    # corr.save(f'../../data/dbins/cxi/run{run}_qcor.dbin')








##### PADFCORR CORRELATION


for run in runs:
    print(f'####### Run {run}')

    pk = scorpy.PeakData(f'{scorpy.DATADIR}/cxi/run{run}_peaks.txt', qmax=qmax)

    run_corr = scorpy.CorrelationVol(nq, npsi, qmax, cos_sample=False)

    frames = pk.split_frames(npeakmax=150)
    nframes = len(frames)

    print('')
    print('############')
    print(f'Filling CorrelationVol from Peakdata via PADFCORR.')
    print(f'Correlating {nframes} frames.')
    print(f'Correlation started: {time.asctime()}\n')

    for frame_i, frame_pk in enumerate(frames):

        print(f'Frame: {frame_i+1}/{nframes}', end='\r')


        im = frame_pk.make_im(r=r, fname=f'/tmp/tmp_frame_im.dbin')


        corr_config = open(f'/tmp/padfcorr_tmp_config.txt', 'w')
        corr_config.write(f'input = /tmp/tmp_frame_im.dbin\n')
        corr_config.write(f'outpath = /tmp\n')
        corr_config.write(f'wavelength = {wavelength}\n')
        corr_config.write(f'pixel_width = {1/res}\n')
        corr_config.write(f'detector_z = {clen}\n')
        corr_config.write(f'nq = {nq}\n')
        corr_config.write(f'nth = {npsi*2}\n')
        corr_config.write(f'tag = padfcorr_tmp_frame\n')
        corr_config.write(f'qmax = {qmax*1e9}\n')
        corr_config.close()

        os.system(f'{scorpy.PADFCORRDIR}padfcorr /tmp/padfcorr_tmp_config.txt')

        tmppadfcorrvol = np.fromfile(f'/tmp/padfcorr_tmp_frame_correlation.dbin')
        tmppadfcorrvol = tmppadfcorrvol.reshape((nq, nq, 2*npsi))

        run_corr.vol += tmppadfcorrvol[:,:, :npsi]

        run_corr.save(f'{scorpy.DATADIR}/dbins/cxi/run{run}_padfcorr_qcor.dbin')

        print('', end='')
    print(f'Correlation finished: {time.asctime()}')
    print('############')





plt.show()



