import numpy as np
import scorpy
import os
import h5py

import utils

import matplotlib.pyplot as plt
plt.close('all')





pk = scorpy.PeakData(h5path=f'{scorpy.DATADIR}/ice/sim/patterns/x.h5', 
                     geompath=f'{scorpy.DATADIR}/ice/sim/geoms/detector.geom')


im = pk.make_im(2001, 0.1)

plt.figure()
plt.imshow(im, clim=(0, np.max(im)/10000000), origin='lower')
# plt.colorbar()


# loc = np.where(pk.scat_rect[:,-1]>1000)

# plt.figure()
# plt.plot(pk.scat_rect[loc[0],0], pk.scat_rect[loc[0],1], ls='', marker='.')
# geom.plot_panels(units='m')
# geom.plot_qring(0.4)



# x = pk.integrate_peaks(0.02)


# loc = np.where(x[:,-1])

# plt.figure()
# plt.plot(x[loc[0],0], x[loc[0],1], ls='', marker='.')
# geom.plot_panels(units='m')
# geom.plot_qring(0.4)






plt.show()

