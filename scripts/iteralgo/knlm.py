
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




cif = scorpy.CifData(f'{scorpy.DATADIR}/cifs/fcc-sf.cif', qmax=qmax)

sphv_mask = scorpy.SphericalVol(nq, ntheta, nphi, qmax)
sphv_mask.fill_from_cif(cif)

sphv_mask.plot_slice(0, 52)
sphv_mask.make_mask()





corr = scorpy.CorrelationVol(nq, npsi, qmax)
corr.fill_from_cif(cif)

blqq = scorpy.BlqqVol(nq, nl, qmax)
blqq.fill_from_corr(corr, inc_odds=True)
lams, us = blqq.get_eig()




iqlm_init = scorpy.IqlmHandler(nq, nl, qmax)
iqlm_init.fill_from_sphv(sphv_mask)
# iqlm_init.vals = np.random.random(iqlm_init.vals.shape)
iqlm_init.mask_l(iqlm_init.nl, 0,2)


sphv_init = scorpy.SphericalVol(nq, ntheta, nphi, qmax)
sphv_init.fill_from_iqlm(iqlm_init)
sphv_init.plot_slice(0,52)


sphv_iter = sphv_init.copy()
iqlm_iter = iqlm_init.copy()


for i in range(4):
    print('iter: ', i, end='\r')



    knlm_iter = iqlm_iter.copy()
    knlm_iter.calc_knlm(us)

    knlmp_iter = knlm_iter.copy()
    knlmp_iter.calc_knlmp(lams)

    iqlmp_iter = knlmp_iter.copy()
    iqlmp_iter.calc_iqlmp(us)

    sphv_iter.fill_from_iqlm(iqlmp_iter)

    # sphv_iter.vol  = np.abs(sphv_iter.vol)
    if i%1==0:
        sphv_iter.plot_slice(0,52)

    sphv_iter.vol *= sphv_mask.vol

    iqlm_iter.fill_from_sphv(sphv_iter)





plt.show()

