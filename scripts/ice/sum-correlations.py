import numpy as np
import scorpy
import os
import sys
import h5py
from datetime import datetime


import matplotlib.pyplot as plt
plt.close('all')




geom =  '19MPz18'

sizes = ['1000nm', '500nm', '250nm', '125nm']


chunk = int(sys.argv[1])


corra = scorpy.CorrelationVol(nq=100, npsi=180,qmin=1.5,qmax=3.1, cos_sample=False)
corrb = scorpy.CorrelationVol(nq=100, npsi=180,qmin=1.5,qmax=3.1, cos_sample=False)

for size in sizes:
    corra.vol *= 0
    corrb.vol *= 0

    print(f'<{datetime.now().strftime("%H:%M:%S")}>: {size=}, {chunk=}')
    for i in range(1, 251, 2):
        corr = scorpy.CorrelationVol(path=f'{scorpy.DATADIR}/ice/sim/corr/{geom}/{size}-qmin15/hex-ice-{size}-qmin15-{geom}-{chunk}-{i}-qcor.npy')
        corrb.vol +=corr.vol

    for i in range(2, 251, 2):
        corr = scorpy.CorrelationVol(path=f'{scorpy.DATADIR}/ice/sim/corr/{geom}/{size}-qmin15/hex-ice-{size}-qmin15-{geom}-{chunk}-{i}-qcor.npy')
        corra.vol +=corr.vol

    corra.save(f'{scorpy.DATADIR}/ice/sim/corr/{geom}/{size}-qmin15/hex-ice-{size}-qmin15-{geom}-{chunk}-a-qcor.npy')
    corrb.save(f'{scorpy.DATADIR}/ice/sim/corr/{geom}/{size}-qmin15/hex-ice-{size}-qmin15-{geom}-{chunk}-b-qcor.npy')





# geom =  '19MPz18'
# size = sys.argv[1]
# print(f'Summing Whole Runs: {size}')


# corra_total = scorpy.CorrelationVol(nq=100, npsi=180,qmin=0.75,qmax=3.1, cos_sample=False)
# corrb_total = scorpy.CorrelationVol(nq=100, npsi=180,qmin=0.75,qmax=3.1, cos_sample=False)

# for chunk in range(1, 161):
    # print(f'<{datetime.now().strftime("%H:%M:%S")}>: {size=}, {chunk=}')

    # corra = scorpy.CorrelationVol(path=f'{scorpy.DATADIR}/ice/sim/corr/{geom}/{size}-qmin75/hex-ice-{size}-qmin75-{geom}-{chunk}-a-qcor.npy')
    # corrb = scorpy.CorrelationVol(path=f'{scorpy.DATADIR}/ice/sim/corr/{geom}/{size}-qmin75/hex-ice-{size}-qmin75-{geom}-{chunk}-b-qcor.npy')

    # corra_total.vol +=corra.vol

    # corrb_total.vol +=corrb.vol

# corra_total.save(f'{scorpy.DATADIR}/ice/sim/corr/hex-ice-{size}-qmin75-{geom}-a-qcor.dbin')
# corrb_total.save(f'{scorpy.DATADIR}/ice/sim/corr/hex-ice-{size}-qmin75-{geom}-b-qcor.dbin')

# corra_total.save(f'{scorpy.DATADIR}/ice/sim/corr/hex-ice-{size}-qmin75-{geom}-a-qcor.npy')
# corrb_total.save(f'{scorpy.DATADIR}/ice/sim/corr/hex-ice-{size}-qmin75-{geom}-b-qcor.npy')


















