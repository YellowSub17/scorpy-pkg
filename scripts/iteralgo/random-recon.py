
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
# qmax = 1.5

lq = 60
qq = 92


cif = scorpy.CifData(f'{scorpy.DATADIR}/cifs/fcc-sf.cif', qmax=qmax)
sphv = scorpy.SphericalVol(nq, ntheta, nphi, qmax)
sphv.fill_from_cif(cif)

sphv.plot_slice(0, qq, title='CIF')
sphv_mask = sphv.copy()
sphv_mask.make_mask()






iqlm_targ = scorpy.IqlmHandler(nq, nl, qmax)
iqlm_targ.fill_from_sphv(sphv)
sphv_targ = sphv.copy()
sphv_targ.fill_from_iqlm(iqlm_targ)
sphv_targ.plot_slice(0, qq, title='Target')
blqq = scorpy.BlqqVol(nq, nl, qmax)
blqq.fill_from_iqlm(iqlm_targ)
lams, us = blqq.get_eig()
lams, us = np.real(lams), np.real(us)



iqlm_rand = scorpy.IqlmHandler(nq, nl, qmax)
# loc = np.where(iqlm_targ.vals !=0)
# iqlm_rand.vals[loc] = np.random.random(iqlm_rand.vals.shape)[loc]
iqlm_rand.vals = np.random.random(iqlm_rand.vals.shape)



sphv_iter = scorpy.SphericalVol(nq, ntheta, nphi, qmax)
sphv_iter.fill_from_iqlm(iqlm_rand)
sphv_iter.plot_slice(0, qq, title=f'0')
iqlm_iter = iqlm_rand.copy()

for i in range(10):
    print(i)
    knlm = iqlm_iter.copy()
    knlm.calc_knlm(us)
    knlmp = knlm.copy()
    knlmp.calc_knlmp(lams)
    iqlm_iter = knlmp.copy()
    iqlm_iter.calc_iqlmp(us)
    sphv_iter.fill_from_iqlm(iqlm_iter)

    sphv_iter.plot_slice(0, qq, title=f'{i+1}')
    sphv_iter.vol *= sphv_mask.vol
    iqlm_iter.fill_from_sphv(sphv_iter)




iqlmp = iqlm_iter.copy()



fig, axes = plt.subplots(1,3, sharex=True, sharey=True)
iqlm_targ.plot_q(qq, fig=fig, axes=axes[0], title='Target')
iqlm_rand.plot_q(qq, fig=fig, axes=axes[1], title='Random Initial')
iqlmp.plot_q(qq, fig=fig, axes=axes[2], title='Final')




plt.show()

