import numpy as np
import scorpy
import os
import h5py

import glob

import matplotlib.pyplot as plt
plt.close('all')


geom= '19MPz18'
size = '125nm'



datapaths = [f'/media/pat/datadrive/ice/sim/patterns/{geom}/{size}/hex-ice-{size}-{geom}-1-{i}.npz' for i in range(1,241)]
datapaths += [f'/media/pat/datadrive/ice/sim/patterns/{geom}/{size}/hex-ice-{size}-{geom}-2-{i}.npz' for i in range(1,241)]
datapaths += [f'/media/pat/datadrive/ice/sim/patterns/{geom}/{size}/hex-ice-{size}-{geom}-3-{i}.npz' for i in range(1,241)]

pk = scorpy.PeakData(datapath=datapaths,
                    geompath=f'/media/pat/datadrive/ice/sim/geoms/{geom}.geom')

# pk.plot_peaks()
# pk.plot_qring(1.2)
# pk.plot_qring(3)

corr = scorpy.CorrelationVol(nq=100, npsi=180, qmax=3, qmin=1)

for datapath in datapaths:
    pk = scorpy.PeakData(datapath=datapath,
                        geompath=f'/media/pat/datadrive/ice/sim/geoms/{geom}.geom')

    inte = pk.integrate_peaks(0.005)
    pk.calc_scat(inte[:,0:3], inte[:,-1])







    corr.fill_from_peakdata(pk, verbose=0)

# pk = scorpy.PeakData(datapath=datapath,
                    # geompath=f'/media/pat/datadrive/ice/sim/geoms/{geom}.geom')

# pk.plot_peaks()
# pk.plot_peakr(0.005)

# inte = pk.integrate_peaks(0.005)
# pk.calc_scat(inte[:,0:3], inte[:,-1])

# pk.plot_peaks()
# pk.plot_peakr(0.005)



corr.plot_sumax(0)



corr = scorpy.CorrelationVol(path=f'/media/pat/datadrive/ice/sim/corr/hex-ice-{size}-19MPz18-a-qcor.npy')


corr.plot_sumax(0)






plt.show()
