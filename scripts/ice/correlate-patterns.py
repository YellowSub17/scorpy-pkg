import numpy as np
import scorpy
import os
import sys
import h5py
from datetime import datetime


import matplotlib.pyplot as plt
plt.close('all')


geom =  '19MPz18'
# sizes = ['1000nm', '500nm', '250nm', '125nm']

# nproc = int(sys.argv[2])
# procs = int(sys.argv[1])

# chunks = [i+nproc-1 for i in range(1, 161, procs)]





# print('Correlating Chunks:')
# print(chunks)

# for size in sizes:

    # for chunk in chunks:
        # print(f'<{datetime.now().strftime("%H:%M:%S")}>: {size=}, {chunk=}')
        # for i in range(1, 251):

            # pk1 = scorpy.PeakData(datapath=f'{scorpy.DATADIR}/ice/sim/patterns/{geom}/{size}/hex-ice-{size}-{geom}-{chunk}-{i}.npz',
                                 # geompath=f'{scorpy.DATADIR}/ice/sim/geoms/{geom}.geom')


            # inte = pk1.integrate_peaks(0.005)
            # pk1.calc_scat(inte[:,0:3], inte[:,-1])

            # corr = scorpy.CorrelationVol(nq=100, npsi=180,qmin=0.75,qmax=3.1, cos_sample=False)
            # corr.fill_from_peakdata(pk1,verbose=0)
            # corr.save(fpath=f'{scorpy.DATADIR}/ice/sim/corr/{geom}/{size}-qmin75/hex-ice-{size}-qmin75-{geom}-{chunk}-{i}-qcor.npy')



size = sys.argv[3]
nproc = int(sys.argv[2])
procs = int(sys.argv[1])

chunks = [i+nproc-1 for i in range(1, 161, procs)]


print('Summing Chunks:')
print(chunks)




for chunk in chunks:

    corra = scorpy.CorrelationVol(nq=100, npsi=180,qmin=0.75,qmax=3.1, cos_sample=False)
    corrb = scorpy.CorrelationVol(nq=100, npsi=180,qmin=0.75,qmax=3.1, cos_sample=False)

    print(f'<{datetime.now().strftime("%H:%M:%S")}>: {size=}, {chunk=}')
    for i in range(1, 251):

        corr = scorpy.CorrelationVol(path=f'{scorpy.DATADIR}/ice/sim/corr/{geom}/{size}-qmin75/hex-ice-{size}-qmin75-{geom}-{chunk}-{i}-qcor.npy')

        if i %2 ==0:
            corra.vol +=corr.vol
        else:

            corrb.vol +=corr.vol

    corra.save(f'{scorpy.DATADIR}/ice/sim/corr/{geom}/{size}-qmin75/hex-ice-{size}-qmin75-{geom}-{chunk}-a-qcor.npy')
    corrb.save(f'{scorpy.DATADIR}/ice/sim/corr/{geom}/{size}-qmin75/hex-ice-{size}-qmin75-{geom}-{chunk}-b-qcor.npy')
















