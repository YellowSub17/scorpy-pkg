

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



# sphv = scorpy.SphericalVol(nq, ntheta, nphi, qmax)
# sphv.vol = np.random.random(sphv.vol.shape)


sphv = sphv_targ.copy()
sphv.vol *= 100
# sphv.vol -=  np.mean(sphv.vol)
sphv.vol += np.random.random(sphv.vol.shape)

sphv.plot_slice(0, qq)


iqlm = scorpy.IqlmHandler(nq, nl, qmax)
iqlm.fill_from_sphv(sphv)
iqlm.plot_q(qq, title=f'initial (nq={nq})')


# iqlm.vals[:,0,:,:] = 0


knlm = iqlm.copy()
knlm.calc_knlm(us)


knlmp = knlm.copy()
# knlmp.calc_knlmp(lams)


iqlmp = knlmp.copy()
iqlmp.calc_iqlmp(us)


iqlmp.plot_q(qq, title=f'iter1 (nq={nq}')



iqlmd = iqlmp.copy()
iqlmd.vals -= iqlm.vals

iqlmd.plot_q(qq, title=f'diff (nq={nq})')




plt.show()












