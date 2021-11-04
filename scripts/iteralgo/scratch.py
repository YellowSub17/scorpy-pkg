

import numpy as np
import scorpy
import matplotlib.pyplot as plt
plt.close('all')
np.random.seed(0)




# Parameters
nq= 100
ntheta = 180
nphi = 360
nl = 90

qmax = 89

qq = 72




# SET UP MASK DATA
cif_supp = scorpy.CifData(f'{scorpy.DATADIR}/cifs/ccc-sf.cif', qmax = qmax)
sphv_supp = scorpy.SphericalVol(nq, ntheta, nphi, qmax)
sphv_supp.fill_from_cif(cif_supp)
sphv_supp.make_mask()
sphv_supp.plot_slice(0, qq, title='support')
loc = np.where(sphv_supp.vol>0)
q_loc1 = np.unique(loc[0])


# SET UP TARGET DATA
cif_targ = scorpy.CifData(f'{scorpy.DATADIR}/cifs/bcc-sf.cif', qmax = qmax)
sphv_targ = scorpy.SphericalVol(nq, ntheta, nphi, qmax)
sphv_targ.fill_from_cif(cif_targ)
loc = np.where(sphv_targ.vol>0)
q_loc2 = np.unique(loc[0])

# add noise
sphv_targ.vol *= 100
sphv_targ.vol[loc] += 2*np.random.random(sphv_targ.vol.shape)[loc]

sphv_targ.plot_slice(0, qq, title='target')


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




# SET UP ALGORITHM
a = scorpy.AlgoHandler(blqq_data, sphv_supp,
                       lossy_sphv=True, lossy_iqlm=True, rcond=1e-3)



# a.sphv_iter = sphv_targ.copy()


iqlm = iqlm_targ.copy()

iqlm.plot_q(qq)

for i in range(20):
    print(i)
    a.ER()


a.iqlmp.plot_q(qq)
a.sphv_iter.plot_slice(0, qq)



# x = iqlmp.vals - iqlm.vals





plt.show()












