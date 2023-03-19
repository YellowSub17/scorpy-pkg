import numpy as np
import scorpy
import os
import sys
import h5py
from datetime import datetime


import matplotlib.pyplot as plt
plt.close('all')


geom =  '19MPz18'
sizes = ['500nm', '250nm', '125nm']



blockstart = int(sys.argv[1])
blockend = blockstart +40


print(f'correlating chunks {blockstart} to {blockend -1}')


for size in sizes:

    corra = scorpy.CorrelationVol(100, 180, 3.1, cos_sample=False)
    corrb = scorpy.CorrelationVol(100, 180, 3.1, cos_sample=False)




    for chunk in range(blockstart, blockend):
        print(f'{datetime.now().strftime("%H:%M:%S")}')
        print(f'{size=}, {chunk=}')
        for i in range(1, 251):

            pk1 = scorpy.PeakData(datapath=f'{scorpy.DATADIR}/ice/sim/patterns/{geom}/{size}/hex-ice-{size}-{geom}-{chunk}-{i}.npz',
                                 geompath=f'{scorpy.DATADIR}/ice/sim/geoms/{geom}.geom')


            inte = pk1.integrate_peaks(0.005)
            pk1.calc_scat(inte[:,0:3], inte[:,-1])


            corr = scorpy.CorrelationVol(100, 180, 3.1, cos_sample=False)
            corr.fill_from_peakdata(pk1,verbose=0)
            corr.save(fpath=f'{scorpy.DATADIR}/ice/sim/corr/{geom}/{size}/hex-ice-{size}-{geom}-{chunk}-{i}-qcor.npy')






            if i%2==0:
                corra.vol +=corr.vol
            else:
                corrb.vol +=corr.vol




    corra.save(f'{scorpy.DATADIR}/ice/sim/corr/hex-ice-{size}-{geom}-a-qcor.npy')
    corrb.save(f'{scorpy.DATADIR}/ice/sim/corr/hex-ice-{size}-{geom}-b-qcor.npy')













