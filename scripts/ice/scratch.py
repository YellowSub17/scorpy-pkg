import numpy as np
import scorpy
import os
import h5py


import matplotlib.pyplot as plt
plt.close('all')


# im = np.zeros( (1000,1000) )

# for i in range(1,321):
    # print(i, end='\r')
    # pk = scorpy.PeakData(datapath=f'{scorpy.DATADIR}/ice/sim/patterns/hex-ice-1um-{i}.coo.npz', 
                         # geompath=f'{scorpy.DATADIR}/ice/sim/geoms/det-1MP-panel.geom')

    # pkim = pk.make_im(1000, 0.1)
    # im +=pkim

# fig, axes = plt.subplots(1,2)
# axes[0].imshow(im, origin='lower')
# axes[1].imshow(pkim, origin='lower')








pk = scorpy.PeakData(datapath=f'{scorpy.DATADIR}/ice/sim/patterns/hex-ice-1um-925.coo.npz', 
                     geompath=f'{scorpy.DATADIR}/ice/sim/geoms/det-1MP-panel.geom')


pk.plot_peaks(peakr=0.005)
pk.plot_qring(1.61)
pk.plot_qring(2.35)




inte = pk.integrate_peaks(0.005)

pk.calc_scat(inte[:,0:3], inte[:,-1])
pk.plot_peaks(peakr=0.005)
pk.plot_qring(1.61)
pk.plot_qring(2.35)



corr = scorpy.CorrelationVol(100, 180, 2.85, cos_sample=False)

corr.fill_from_peakdata(pk,verbose=99)


corr.plot_sumax(1, vminmax=(0, corr.vol.max()/100))


corr.save(fpath=f'{scorpy.DATADIR}/ice/sim/corr/xc.npy')
corr.save(fpath=f'{scorpy.DATADIR}/ice/sim/corr/xd.dbin')


corr2 = scorpy.CorrelationVol(path=f'{scorpy.DATADIR}/ice/sim/corr/xc.npy')
corr3 = scorpy.CorrelationVol(path=f'{scorpy.DATADIR}/ice/sim/corr/xd.dbin')












plt.show()

