

import numpy as np
import scorpy
import matplotlib.pyplot as plt
plt.close('all')
np.random.seed(0)




# Parameters
nq= 450
ntheta = 180
nphi = 360
nl = 90

qmax = 89





# SET UP MASK DATA
cif_supp = scorpy.CifData(f'{scorpy.DATADIR}/cifs/ccc-sf.cif', qmax = qmax)
sphv_supp = scorpy.SphericalVol(nq, ntheta, nphi, qmax)
sphv_supp.fill_from_cif(cif_supp)
sphv_supp.make_mask()


# SET UP TARGET DATA
cif_targ = scorpy.CifData(f'{scorpy.DATADIR}/cifs/ccc-sf.cif', qmax = qmax)
sphv_targ = scorpy.SphericalVol(nq, ntheta, nphi, qmax)
sphv_targ.fill_from_cif(cif_targ)

loc = np.where(sphv_targ.vol>0)
q_inds = np.unique(loc[0])
qq = q_inds[-4]



# get harmonic coefficients
iqlm_targ = scorpy.IqlmHandler(nq, nl, qmax)
iqlm_targ.fill_from_sphv(sphv_targ)

# get harmonic filtered bragg spots
sphv_harmed = scorpy.SphericalVol(nq, ntheta, nphi, qmax)
sphv_harmed.fill_from_iqlm(iqlm_targ)

# SET UP BLQQ
blqq_data = scorpy.BlqqVol(nq, nl, qmax)
blqq_data.fill_from_iqlm(iqlm_targ)




# # # SET UP ALGORITHM
a = scorpy.AlgoHandler(blqq_data, sphv_supp, lossy_sphv=True, lossy_iqlm=True, rcond=1)



# iqlmx = scorpy.IqlmHandler(nq,nl, qmax)
# iqlmx.fill_from_sphv(a.sphv_iter)
# sphvx = scorpy.SphericalVol(nq, ntheta, nphi, qmax)
# sphvx.fill_from_iqlm(iqlmx)
# a.sphv_iter = sphvx.copy()

# a.sphv_iter = sphv_harmed.copy()


# a.sphv_iter.vol *= sphv_supp.vol




sphv_i, sphv_f = a._Pm()

sphv_d = sphv_f.copy()
sphv_d.vol -=sphv_i.vol


iqlm = a.iqlm_iter.copy()
iqlmp = a.iqlm_add.copy()

iqlmd = iqlmp.copy()
iqlmd.vals -= iqlm.vals





fig, axes = plt.subplots(3,3)
plt.suptitle('pm')
sphv_i.plot_slice(0, qq, title='initial', fig=fig, axes=axes[0,0])
sphv_f.plot_slice(0, qq, title='final', fig=fig, axes=axes[0,1])
sphv_d.plot_slice(0, qq, title='diff', fig=fig, axes=axes[0,2])



iqlm.plot_q(qq, title='initial', fig=fig, axes=axes[1,0])
iqlmp.plot_q(qq, title='final', fig=fig, axes=axes[1,1])
iqlmd.plot_q(qq, title='diff', fig=fig, axes=axes[1,2])

iqlm.vals[:,0,0,0] = 0
iqlmp.vals[:,0,0,0] = 0
iqlmd.vals[:,0,0,0] = 0

iqlm.plot_q(qq, title='initial l0=0', fig=fig, axes=axes[2,0])
iqlmp.plot_q(qq, title='final l0=0', fig=fig, axes=axes[2,1])
iqlmd.plot_q(qq, title='diff l0=0', fig=fig, axes=axes[2,2])




plt.show()







