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
nl = 60
l=10



cif = scorpy.CifData('../data/xtal/1al1-sf.cif', qmax)






corr = scorpy.CorrelationVol(nq, nangle, cif.qmax)
corr.fill_from_cif(cif,'scat_rect')
corr.plot_q1q2()
plt.title('Original corr q1=q2')

blqq1 = scorpy.BlqqVol(nq, nl, cif.qmax)
blqq1.fill_from_corr(corr)
blqq1.plot_slice(axis=2, index=l, extent=None)
plt.title(f"Blqq, l={l}, from corr")

corr1 = scorpy.CorrelationVol(nq, nangle, cif.qmax)
corr1.fill_from_blqq(blqq1)
corr1.plot_q1q2()
plt.title('Corr, from blqq from corr')





sphv = scorpy.SphericalVol(nq, nangle, cif.qmax)
sphv.fill_from_cif(cif)

blqq2 = scorpy.BlqqVol(nq,nl, cif.qmax)
blqq2.fill_from_sphv(sphv)
blqq2.plot_slice(axis=2, index=l, extent=None)
plt.title(f"Blqq, l={l}, from sphv")

corr2 = scorpy.CorrelationVol(nq, nangle, cif.qmax)
corr2.fill_from_blqq(blqq2)
corr2.plot_q1q2()
plt.title('Corr, from blqq from sphv')






sph = scorpy.SphHarmHandler(nq,nl,cif.qmax)
sph.fill_from_cif(cif)

blqq3 = scorpy.BlqqVol(nq, nl, cif.qmax)
blqq3.fill_from_sph(sph)
blqq3.plot_slice(axis=2, index=l, extent=None)
plt.title(f"Blqq, l={l}, from sph")

corr3 = scorpy.CorrelationVol(nq, nangle, cif.qmax)
corr3.fill_from_blqq(blqq3)
corr3.plot_q1q2()
plt.title('Corr, from blqq from sphv')












plt.show()






