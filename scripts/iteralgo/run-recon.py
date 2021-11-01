#!/usr/bin/env python3
'''
solved-test.py

replaces the initial spherical volume object with the target solution,
and ensures the same values are returned after one iteration.
'''
import scorpy
import numpy as np
import matplotlib.pyplot as plt
import time
plt.close('all')


np.random.seed(0)







# Parameters
nq= 100
ntheta = 180
nphi = 360
nl = 90

# ntheta = 20
# nphi = 40
# nl = 10
qmax = 108
qmax = 89

qq = 50



# SET UP MASK DATA
cif_mask = scorpy.CifData(f'{scorpy.DATADIR}/cifs/ccc-sf.cif', qmax = qmax)
sphv_mask = scorpy.SphericalVol(nq, ntheta, nphi, qmax)
sphv_mask.fill_from_cif(cif_mask)
sphv_mask.make_mask()


# SET UP TARGET DATA
cif_targ = scorpy.CifData(f'{scorpy.DATADIR}/cifs/fcc-sf.cif', qmax = qmax)
sphv_targ = scorpy.SphericalVol(nq, ntheta, nphi, qmax)
sphv_targ.fill_from_cif(cif_targ)
loc = np.where(sphv_targ.vol>0)

# add noise
sphv_targ.vol *= 10
sphv_targ.vol[loc] += 3*np.random.random(sphv_targ.vol.shape)[loc]
sphv_targ.vol += np.random.random(sphv_targ.vol.shape)

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




# SET UP ALGORITHM
a = scorpy.AlgoHandler(blqq_data, sphv_mask,
                       lossy_sphv=True, lossy_iqlm=True, rcond=1e-3)


a.sphv_iter = sphv_targ.copy()


a.sphv_iter.plot_slice(0, qq, title='initial')
a.DM()
a.sphv_iter.plot_slice(0, qq, title='iter1')
a.DM()
a.sphv_iter.plot_slice(0, qq, title='iter2')

plt.show()















