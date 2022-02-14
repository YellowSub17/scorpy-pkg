import numpy as np
import h5py

import scorpy

import matplotlib.pyplot as plt
plt.close('all')













geo = scorpy.ExpGeom(f'{scorpy.DATADIR}/geoms/single_square.geom', nfs=1000, nss=1000)
pk = scorpy.PeakData(f'{scorpy.DATADIR}/patternsim/test.h5', geo=geo)

# im = pk.make_im(npix= 1000, r=0.5, bool_inten=True)
# plt.figure()
# plt.imshow(im)



pk.plot_peaks()


corr = scorpy.CorrelationVol(qmax=pk.qmax)
corr.fill_from_peakdata(pk)

corr.plot_q1q2()




scorpy.utils.blockPrint()
print("This won't")

scorpy.utils.enablePrint()
print("This will too")


plt.show()

