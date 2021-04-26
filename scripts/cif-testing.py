import scorpy
import matplotlib.pyplot as plt
plt.close('all')

import timeit


from scorpy.utils import angle_between_sph
import numpy as np





qmax = 0.36992983463258367/3
# qmax = None
nq = 100
nangle = 180
nl = 85
l=10



cif = scorpy.CifData('../data/xtal/1al1-sf.cif', qmax)

corr = scorpy.CorrelationVol(nq, nangle, cif.qmax)
corr.fill_from_cif(cif,'scat_rect')

blqq1 = scorpy.BlqqVol(nq, nl, cif.qmax)
blqq1.fill_from_corr(corr)
blqq1.plot_slice(axis=2, index=l, extent=None)
plt.title(f"Blqq, l={l}, from corr")


print("Intensity at q=", np.unique(np.where(blqq1.vol>0)[0]))




sphv = scorpy.SphericalVol(nq, nangle, cif.qmax)
sphv.fill_from_cif(cif)

# sphv.plot_sumax(axis=0)


blqq2 = scorpy.BlqqVol(nq,nl, cif.qmax)
blqq2.fill_from_sphv(sphv)
blqq2.plot_slice(axis=2, index=l, extent=None)
plt.title(f"Blqq, l={l}, from sphv")



plt.show()






