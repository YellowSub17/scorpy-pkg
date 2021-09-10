
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

sphv = scorpy.SphericalVol(nq, ntheta, nphi, qmax)
sphv.fill_from_cif(cif)
sphv.make_mask()


iqlm = scorpy.IqlmHandler(nq, nl, qmax)
iqlm.fill_from_sphv(sphv)

corr = scorpy.CorrelationVol(nq, npsi, qmax)
corr.fill_from_cif(cif)

blqq = scorpy.BlqqVol(nq, nl, qmax)
blqq.fill_from_corr(corr)
lams, us = blqq.get_eig()




iqlm1 = scorpy.IqlmHandler(nq, nl, qmax)
iqlm1.vals = np.random.random(iqlm1.vals.shape)


for i in range(10):
    print('iter: ', i)


    sphv1 = scorpy.SphericalVol(nq, ntheta, nphi, qmax)
    sphv1.fill_from_iqlm(iqlm1)
    sphv1.vol *= sphv.vol
    sphv1.plot_slice(0, 52)


    knlm = iqlm1.copy()
    knlm.calc_knlm(us)

    knlmp = knlm.copy()
    knlmp.calc_knlmp(lams)

    iqlm1 = knlmp.copy()
    iqlm1.calc_iqlmp(us)



corr.plot_q1q2()
sphv.plot_slice(0, 52)
sphv1.plot_slice(0, 52)



plt.show()




# sphv1 = scorpy.SphericalVol(nq,ntheta, nphi, qmax)
# sphv1.fill_from_iqlm(iqlm)


# # get the harmonic order matrix
# blqq = scorpy.BlqqVol(nq, nl, qmax)
# blqq.fill_from_iqlm(iqlm, inc_odds=True)

# # get eigenvalues and vectors
# lams, us = blqq.get_eig(herm=True)



# # knlm -> iqlm prime calculation
# knlm = iqlm.copy()
# knlm.calc_knlm(us)

# knlm_loc = np.where(knlm.vals != 0)





# knlmp = knlm.copy()
# knlmp.calc_knlmp(lams)


# iqlmp = knlmp.copy()
# iqlmp.calc_iqlmp(us)

# iqlmp_loc = np.where(iqlmp.vals != 0)



# # replot harmonics on new spherical volume
# sphv2 = scorpy.SphericalVol(nq,ntheta, nphi, qmax)
# sphv2.fill_from_iqlm(iqlmp)

# sphv_diff = sphv2.copy()
# sphv_diff.vol -= sphv1.vol


# qs = [40]
# for q_ind in qs:
    # fig, axes = plt.subplots(1,3)
    # plt.suptitle(f'q shell {q_ind}')
    # sphv1.plot_slice(0, q_ind, fig=fig, axes=axes[0], title='Before')
    # sphv2.plot_slice(0, q_ind, fig=fig, axes=axes[1], title='After')
    # sphv_diff.plot_slice(0, q_ind, fig=fig, axes=axes[2], title='Difference')






plt.show()
