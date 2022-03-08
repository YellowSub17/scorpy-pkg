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


geompath = f'{scorpy.DATADIR}/geoms/agipd_2304_vj_opt_v4.geom'
pdbpath = f'{scorpy.DATADIR}/xtal/1vds.pdb'
hklpath = f'{scorpy.DATADIR}/xtal/1vds.hkl'



nframes = [2**i for i in range(9, 12)]
nframes = [2, 4, 8, 16, 512, 1024, 2048]






geo = scorpy.ExpGeom(f'{geompath}')





#### SCORPY CORRELATION
for n in nframes:


    for file in os.listdir('/tmp/'):
        if 'euxfel-simcorr' in file:
            os.remove(f'/tmp/{file}')


    print(f'######Generating {n} frames. {time.asctime()}')
    cmd = f"pattern_sim -g {geompath} -p {pdbpath} -r --really-random --number={n} -i {hklpath} --photon-energy 9300 --gpu --min-size=500 --max-size=500 -o /tmp/euxfel-simcorr-{n}"
    os.system(f'{cmd} >/tmp/euxfel-simcorr-patternsim.log 2>&1')


    print(f'Correlating frames. {time.asctime()}')
    corr = scorpy.CorrelationVol(nq=nq, npsi=npsi, qmax=qmax, cos_sample=False)
    for frame in range(n):
        pk = scorpy.PeakData(f'/tmp/euxfel-simcorr-{n}-{frame+1}.h5', qmax=qmax, geo = geo)



        print(f'\x1b[2Ka Frame {frame}', end='\r')
        corr.fill_from_peakdata(pk)


    corr.save(f'{scorpy.DATADIR}/dbins/cxi/qcors/sim/{n}/sim{n}-qcor.dbin')





    print()
    for seed in range(20):

        print(f'n: {n}.')
        print(f'Seed: {seed}.')
        print(f'Time: {time.asctime()}.')
        corra = scorpy.CorrelationVol(nq=nq, npsi=npsi, qmax=qmax, cos_sample=False)

        frames_shuffled = np.arange(1, n+1)
        np.random.shuffle(frames_shuffled)

        for i, seed_i in enumerate(frames_shuffled[:int(n/2)]):

            pk = scorpy.PeakData(f'/tmp/euxfel-simcorr-{n}-{seed_i}.h5', qmax=qmax, geo=geo )

            print(f'\x1b[2Ka Frame {i+1}', end='\r')
            corra.fill_from_peakdata(pk)
        corra.save(f'{scorpy.DATADIR}/dbins/cxi/qcors/sim/{n}/sim{n}-seed{seed}a-qcor.dbin')

        corrb = scorpy.CorrelationVol(nq=nq, npsi=npsi, qmax=qmax, cos_sample=False)

        for i, seed_i in enumerate(frames_shuffled[int(n/2):]):

            pk = scorpy.PeakData(f'/tmp/euxfel-simcorr-{n}-{seed_i}.h5', qmax=qmax, geo=geo )

            print(f'\x1b[2Kb Frame {i+1}', end='\r')
            corrb.fill_from_peakdata(pk)
        corrb.save(f'{scorpy.DATADIR}/dbins/cxi/qcors/sim/{n}/sim{n}-seed{seed}b-qcor.dbin')
        print()















pk.plot_peaks()






plt.show()












