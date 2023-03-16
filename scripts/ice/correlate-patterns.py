import numpy as np
import scorpy
import os
import sys
import h5py


import matplotlib.pyplot as plt
plt.close('all')


geom =  '19MPz18'
size = '1000nm'



# blockstart = int(sys.argv[1])



# for chunk in range(blockstart, blockstart+81):
    # print(chunk)
    # for i in range(1, 251):

        # pk1 = scorpy.PeakData(datapath=f'{scorpy.DATADIR}/ice/sim/patterns/{geom}/{size}/hex-ice-{size}-{geom}-{chunk}-{i}.npz',
                             # geompath=f'{scorpy.DATADIR}/ice/sim/geoms/{geom}.geom')


        # inte = pk1.integrate_peaks(0.005)
        # pk1.calc_scat(inte[:,0:3], inte[:,-1])


        # corr = scorpy.CorrelationVol(100, 180, 3.1, cos_sample=False)
        # corr.fill_from_peakdata(pk1,verbose=0)
        # corr.save(fpath=f'{scorpy.DATADIR}/ice/sim/corr/{geom}/{size}/hex-ice-{size}-{geom}-{chunk}-{i}-qcor.npy')








corra = scorpy.CorrelationVol(100, 180, 3.1, cos_sample=False)
corrb = scorpy.CorrelationVol(100, 180, 3.1, cos_sample=False)



for chunk in range(1,161):
    for i in range(1, 251):
        print(chunk, i)
        corr = scorpy.CorrelationVol(path=f'{scorpy.DATADIR}/ice/sim/corr/{geom}/{size}/hex-ice-{size}-{geom}-{chunk}-{i}-qcor.npy')
        if i%2==0:
            corra.vol +=corr.vol
        else:
            corrb.vol +=corr.vol




corra.save(f'{scorpy.DATADIR}/ice/sim/corr/hex-ice-1000nm-{geom}-a-qcor.npy')
corrb.save(f'{scorpy.DATADIR}/ice/sim/corr/hex-ice-1000nm-{geom}-b-qcor.npy')













