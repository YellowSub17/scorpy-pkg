

import scorpy
import numpy as np
import matplotlib.pyplot as plt
plt.close('all')






# Parameters
nq= 200
ntheta = 180
nphi = 360
nl = 90
qmax = 108
qq = 60
nn = -2
ll = 40
rcond = 1e-1

# SET UP DATA
cif = scorpy.CifData(f'{scorpy.DATADIR}/cifs/fcc-sf.cif', qmax = qmax)

# SET UP MASK
sphv_mask = scorpy.SphericalVol(nq, ntheta, nphi, qmax)
sphv_mask.fill_from_cif(cif)
sphv_mask.make_mask()

# SET UP TARGET HARMONICS
sphv_targ = sphv_mask.copy()
iqlm_targ = scorpy.IqlmHandler(nq, nl, qmax)
iqlm_targ.fill_from_sphv(sphv_targ)

# SET UP BLQQ
blqq_data = scorpy.BlqqVol(nq, nl, qmax)
blqq_data.fill_from_iqlm(iqlm_targ)


lams, us = blqq_data.get_eig()
lams_lossy, us_lossy = blqq_data.get_eig()

eigs_thresh = np.max(lams_lossy, axis=0)*rcond

for l_ind, eig_thresh in enumerate(eigs_thresh):
    loc = np.where(lams_lossy[:,l_ind] < eig_thresh)
    lams_lossy[loc, l_ind] = 0
    loc = np.where(lams_lossy[:,l_ind] ==0)
    us_lossy[:, loc, l_ind] = 0




x = np.abs(us_lossy[...,ll]).sum(axis=0)
neigs = len(np.where(x>0)[0])


fig, axes = plt.subplots(2,1, sharex=True, sharey=True)
plt.suptitle(f'rcond: {rcond}, #eigs:{neigs}')

axes[0].imshow(us[...,ll])
axes[0].set_title('Evectors before')
axes[1].imshow(us_lossy[...,ll])
axes[1].set_title('Evectors after')


knlm_full = iqlm_targ.copy()
knlm_full.calc_knlm(us)
iqlm_full = knlm_full.copy()
iqlm_full.calc_iqlmp(us)



knlm_lossy = iqlm_targ.copy()
knlm_lossy.calc_knlm(us_lossy)
iqlm_lossy = knlm_lossy.copy()
iqlm_lossy.calc_iqlmp(us_lossy)



iqlm_diff = iqlm_targ.copy()
iqlm_diff.vals -= iqlm_lossy.vals






fig, axes = plt.subplots(2,2, sharex=True, sharey=True)

plt.suptitle(f'rcond: {rcond}, #eigs:{neigs}')
iqlm_targ.plot_q(qq, fig=fig, axes=axes[0,0], title='target')
iqlm_full.plot_q(qq, fig=fig, axes=axes[0,1], title='full')
iqlm_lossy.plot_q(qq, fig=fig, axes=axes[1,0], title='lossy')
iqlm_diff.plot_q(qq, fig=fig, axes=axes[1,1], title='diff')






plt.show()










