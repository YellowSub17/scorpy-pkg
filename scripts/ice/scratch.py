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








pk1 = scorpy.PeakData(datapath=f'{scorpy.DATADIR}/ice/sim/patterns/hex-ice-1um-19.npz', 
                     geompath=f'{scorpy.DATADIR}/ice/sim/geoms/det-1MP-panel.geom')



pk2 = scorpy.PeakData(datapath=f'{scorpy.DATADIR}/ice/sim/patterns/hex-ice-1um-19.npz', 
                     geompath=f'{scorpy.DATADIR}/ice/sim/geoms/det-1MP-panel.geom')

inte = pk2.integrate_peaks(0.005)
pk2.calc_scat(inte[:,0:3], inte[:,-1])




corr = scorpy.CorrelationVol(100, 180, 2.35, cos_sample=False)
corr.fill_from_peakdata(pk2,verbose=99)
corr.plot_sumax(0, vminmax=(0, 1))
corr.save(fpath=f'{scorpy.DATADIR}/ice/sim/corr/xc.npy')





pk2.plot_peaks()
pk2.plot_qring(2.35)
pk2.label_qphi(0.001, 0.001)
for q in corr.ls_pts()[:,0]:
    print('q+-: ', q-corr.dq/2, q, q+corr.dq/2)
    pk2.plot_qring(q)
    pk2.plot_qring(q+corr.dq/2, ec='red')
    pk2.plot_qring(q-corr.dq/2,ec='red')














plt.show()

