

import numpy as np
import scorpy
import matplotlib.pyplot as plt
plt.close('all')
np.random.seed(0)




# Parameters
nq= 250
ntheta = 180
nphi = 360
nl = 90

qmax = 89

qq = 89
qq = 39





# SET UP MASK DATA
cif_supp = scorpy.CifData(f'{scorpy.DATADIR}/cifs/ccc-sf.cif', qmax = qmax)
sphv_supp = scorpy.SphericalVol(nq, ntheta, nphi, qmax)
sphv_supp.fill_from_cif(cif_supp)
sphv_supp.make_mask()
# sphv_supp.plot_slice(0, qq, title='support')


# SET UP TARGET DATA
cif_targ = scorpy.CifData(f'{scorpy.DATADIR}/cifs/ccc-sf.cif', qmax = qmax)
sphv_targ = scorpy.SphericalVol(nq, ntheta, nphi, qmax)
sphv_targ.fill_from_cif(cif_targ)
loc = np.where(sphv_targ.vol>0)
q_loc2 = np.unique(loc[0])



# get harmonic coefficients
iqlm_targ = scorpy.IqlmHandler(nq, nl, qmax)
iqlm_targ.fill_from_sphv(sphv_targ)

# get harmonic filtered bragg spots
sphv_harmed = scorpy.SphericalVol(nq, ntheta, nphi, qmax)
sphv_harmed.fill_from_iqlm(iqlm_targ)

# SET UP BLQQ
blqq_data = scorpy.BlqqVol(nq, nl, qmax)
blqq_data.fill_from_iqlm(iqlm_targ)


lams, us = blqq_data.get_eig()



# # # SET UP ALGORITHM
# # a = scorpy.AlgoHandler(blqq_data, sphv_supp, lossy_sphv=True, lossy_iqlm=True, rcond=1e-3)



# x = us[50,:,10]
# y = us[78,:,10]



# plt.figure()
# plt.imshow(us[...,10])



sphv = scorpy.SphericalVol(nq, ntheta, nphi, qmax)
sphv.vol = np.random.random(sphv.vol.shape)#*sphv_supp.vol

sphv = sphv_harmed.copy()


# iqlmx = scorpy.IqlmHandler(nq, nl, qmax)
# iqlmx.fill_from_sphv(sphv)
# sphv.fill_from_iqlm(iqlmx)


# sphv = sphv_targ.copy()
# sphv.vol *= 100
# sphv.vol -=  np.mean(sphv.vol)
# sphv.vol += np.random.random(sphv.vol.shape)



iqlm = scorpy.IqlmHandler(nq, nl, qmax)
iqlm.fill_from_sphv(sphv)


knlm = iqlm.copy()
knlm.calc_knlm(us)


knlmp = knlm.copy()
# knlmp.calc_knlmp(lams)


iqlmp = knlmp.copy()
iqlmp.calc_iqlmp(us)


sphvp = scorpy.SphericalVol(nq, ntheta, nphi, qmax)
sphvp.fill_from_iqlm(iqlmp)


iqlmd = iqlmp.copy()
iqlmd.vals -= iqlm.vals


fig, axes = plt.subplots(2, 3, sharex=True, sharey=True)

iqlm.plot_q(qq, title='initial', fig=fig, axes=axes[0,0])
iqlmp.plot_q(qq, title='final', fig=fig, axes=axes[0,1])
iqlmd.plot_q(qq, title='diff', fig=fig, axes=axes[0,2])

iqlm.vals[:,0,0,0] = 0
iqlmp.vals[:,0,0,0] = 0
iqlmd.vals[:,0,0,0] = 0

iqlm.plot_q(qq, title='initial l0=0', fig=fig, axes=axes[1,0])
iqlmp.plot_q(qq, title='final l0=0', fig=fig, axes=axes[1,1])
iqlmd.plot_q(qq, title='diff l0=0', fig=fig, axes=axes[1,2])



fig, axes = plt.subplots(1, 2, sharex=True, sharey=True)

sphv.plot_slice(0, qq, title='initial', fig=fig, axes=axes[0])
sphvp.plot_slice(0, qq, title='final', fig=fig, axes=axes[1])



plt.show()












