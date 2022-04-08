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

framesdir = f'{scorpy.DATADIR}/frames'



nframes = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048]
npartitions = [21, 21, 21, 21, 21, 21, 21, 21, 16, 8, 4, 2]
# nparentframes = 4096
nparentframes = 1024



# nframes = [1, 2, 4, 8]
# npartitions = [21, 21, 21, 21]
# nparentframes = 4096







geom = scorpy.ExpGeom(f'{geompath}')



###### Generate Frames
print(f'######Generating {nparentframes} frames. {time.asctime()}')
cmd = f"pattern_sim -g {geompath} -p {pdbpath} -r --really-random --number={nparentframes} -i {hklpath} --photon-energy 9300 --gpu --min-size=500 --max-size=500 -o {framesdir}/euxfel-simcorr-alpha-x"
os.system(f'{cmd} >/tmp/euxfel-simcorr-patternsim.log 2>&1')




# for nframe, npartition in zip(nframes, npartitions):

    # print(f'Nframes: {nframe}, Npartitions: {npartition}')


    # for partition in range(0, npartition):

        # part_start = nframe*partition +1
        # part_end = nframe*partition +nframe

        # print(f'\tPartition {partition}: {part_start} - {part_end}')

        # corrp = scorpy.CorrelationVol(nq, npsi, qmax, cos_sample=False)
        # for frame in range(part_start, part_end+1):

            # pk = scorpy.PeakData(f'{scorpy.DATADIR}/frames/euxfel-simcorr-{frame}.h5', qmax=qmax, geom=geom)

            # corrp.fill_from_peakdata(pk)


        # corrp.save(f'{scorpy.DATADIR}/dbins/cxi/qcors/sim/{nframe}/sim{nframe}-p{partition}-qcor.dbin')































# #### SCORPY CORRELATION
# for n in nframes:

    # for seed in range(20):

        # print(f'n: {n}.')
        # print(f'Seed: {seed}.')
        # # print(f'Time: {time.asctime()}.')
        # corra = scorpy.CorrelationVol(nq=nq, npsi=npsi, qmax=qmax, cos_sample=False)

        # # first half of the random numbers make a
        # for i, seed_i in enumerate(frames_shuffled[:n]):

            # pk = scorpy.PeakData(f'{framesdir}/euxfel-simcorr-{seed_i}.h5', qmax=qmax, geom=geom )

            # corra.fill_from_peakdata(pk)
        # corra.save(f'{scorpy.DATADIR}/dbins/cxi/qcors/sim/{n}/sim{n}-seed{seed}a-qcor.dbin')

        # corrb = scorpy.CorrelationVol(nq=nq, npsi=npsi, qmax=qmax, cos_sample=False)

        # # second half of the random numbers make b
        # for i, seed_i in enumerate(frames_shuffled[n:2*n]):

            # pk = scorpy.PeakData(f'/tmp/euxfel-simcorr-x-{seed_i}.h5', qmax=qmax, geom=geom )

            # corrb.fill_from_peakdata(pk)
        # corrb.save(f'{scorpy.DATADIR}/dbins/cxi/qcors/sim/{n}/sim{n}-seed{seed}b-qcor.dbin')
        # print()




# plt.show()












