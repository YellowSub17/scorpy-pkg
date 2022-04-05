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



geompath = f'{scorpy.DATADIR}/geoms/agipd_2304_vj_opt_v4.geom'
pdbpath = f'{scorpy.DATADIR}/xtal/1vds.pdb'
hklpath = f'{scorpy.DATADIR}/xtal/1vds.hkl'



nframes = [2, 4, 8, 16, 32, 64, 128, 256, 512, 1024]

nparentframes = 2048






geom = scorpy.ExpGeom(f'{geompath}')





# #### clean up
# for file in os.listdir('/tmp/'):
    # if 'euxfel-simcorr' in file:
        # os.remove(f'/tmp/{file}')


# ###### Generate Frames
# print(f'######Generating {nparentframes} frames. {time.asctime()}')
# cmd = f"pattern_sim -g {geompath} -p {pdbpath} -r --really-random --number={nparentframes} -i {hklpath} --photon-energy 9300 --gpu --min-size=500 --max-size=500 -o /tmp/euxfel-simcorr-x"
# os.system(f'{cmd} >/tmp/euxfel-simcorr-patternsim.log 2>&1')

#### SCORPY CORRELATION
for n in nframes:

    for seed in range(20):

        print(f'n: {n}.')
        print(f'Seed: {seed}.')
        # print(f'Time: {time.asctime()}.')
        corra = scorpy.CorrelationVol(nq=nq, npsi=npsi, qmax=qmax, cos_sample=False)


        #numbers 1 to n
        frames_shuffled = np.arange(1, nparentframes+1)
        # numbers 1 to n in a random order
        np.random.shuffle(frames_shuffled)

        # first half of the random numbers make a
        for i, seed_i in enumerate(frames_shuffled[:int(n/2)]):

            pk = scorpy.PeakData(f'/tmp/euxfel-simcorr-x-{seed_i}.h5', qmax=qmax, geom=geom )

            print(f'\x1b[2Ka Frame {i+1}', end='\r')
            corra.fill_from_peakdata(pk)
        corra.save(f'{scorpy.DATADIR}/dbins/cxi/qcors/sim/{n}/sim{n}-seed{seed}a-qcor.dbin')

        corrb = scorpy.CorrelationVol(nq=nq, npsi=npsi, qmax=qmax, cos_sample=False)

        # second half of the random numbers make b
        for i, seed_i in enumerate(frames_shuffled[int(n/2):n]):

            pk = scorpy.PeakData(f'/tmp/euxfel-simcorr-x-{seed_i}.h5', qmax=qmax, geom=geom )

            print(f'\x1b[2Kb Frame {i+1}', end='\r')
            corrb.fill_from_peakdata(pk)
        corrb.save(f'{scorpy.DATADIR}/dbins/cxi/qcors/sim/{n}/sim{n}-seed{seed}b-qcor.dbin')
        print()















pk.plot_peaks()






plt.show()












