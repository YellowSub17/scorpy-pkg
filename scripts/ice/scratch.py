import numpy as np
import scorpy
import os
import h5py

import utils

import matplotlib.pyplot as plt
plt.close('all')




utils.gen_pattern(size=1e4, nph=1e12)

pk = scorpy.PeakData(h5path=f'{scorpy.DATADIR}/ice/sim/patterns/x.h5', 
                     geompath=f'{scorpy.DATADIR}/ice/sim/geoms/detector.geom')




im = pk.make_im(1000, 0.1)

plt.figure()
plt.imshow(np.log10(np.abs(im)+1),  origin='lower')
plt.colorbar()





# corr = scorpy.CorrelationVol(nq=200, npsi=360,qmax=2.25, cos_sample=False)

# corr.fill_from_detector_imgs([ im ], int(im.shape[0]/2), int(im.shape[0]/2))

# # corr.plot_q1q2( vminmax=(0, 4e15) )

# tmean = corr.zmean_subtraction()

# corr.plot_q1q2()

# pk.plot_peaks(intenthresh=1)
# pk.plot_qring(q=1)
# pk.plot_qring(q=0.8)
# pk.plot_qring(q=2.0)
# pk.plot_panels()
# for q in corr.qpts[::10]:
    # pk.plot_qring(q)











plt.show()

