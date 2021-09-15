
import numpy as np
np.random.seed(0)
import random
import pyshtools as pysh
import matplotlib.pyplot as plt
plt.close('all')

import scorpy

nq = 100
nphi = 360
ntheta = 180
npsi = 180
nl = int(ntheta/2)

qmax = 40

lq = 60
qq = 92


cif = scorpy.CifData(f'{scorpy.DATADIR}/cifs/fcc-sf.cif', qmax=qmax)
sphv = scorpy.SphericalVol(nq, ntheta, nphi, qmax)
sphv.fill_from_cif(cif)
sphv.plot_slice(0, qq, title='From CIF')





corr = scorpy.CorrelationVol(nq, npsi, qmax)
corr.fill_from_cif(cif)

blqq = scorpy.BlqqVol(nq, nl, qmax)
blqq.fill_from_corr(corr, inc_odds=True)
lams, us = blqq.get_eig(herm=True)

lams, us = np.real(lams), np.real(us)







iqlm1 = scorpy.IqlmHandler(nq, nl, qmax)
iqlm1.fill_from_sphv(sphv)
# iqlm1.mask_l(iqlm1.nl, 0,2)
iqlm1.plot_q(qq, title=f'q={qq}')
iqlm1.plot_l(lq, title=f'l={lq}')


sphv1 = sphv.copy()
sphv1.fill_from_iqlm(iqlm1)
sphv1.plot_slice(0, qq, title=f'q={qq}')



knlm1 = iqlm1.copy()
knlm1.calc_knlm(us)

knlmp1 = knlm1.copy()
knlmp1.calc_knlmp(lams)





iqlmp1 = knlmp1.copy()
iqlmp1.calc_iqlmp(us)
iqlmp1.plot_q(qq, title=f'q={qq}')
iqlmp1.plot_l(lq, title=f'l={lq}')





sphv2 = sphv1.copy()
sphv2.fill_from_iqlm(iqlmp1)
sphv2.plot_slice(0,qq)


sphv_diff1 = sphv2.copy()
sphv_diff1.vol -= sphv1.vol

sphv_diff1.plot_slice(0,52)




plt.show()

