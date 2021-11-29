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
import os
plt.close('all')


np.random.seed(2)



# Parameters
nq= 200
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
cif_targ = scorpy.CifData(f'{scorpy.DATADIR}/cifs/fcc-sf.cif', qmax = qmax)
sphv_targ = scorpy.SphericalVol(nq, ntheta, nphi, qmax)
sphv_targ.fill_from_cif(cif_targ)


loc = np.where(sphv_targ.vol>0)
q_inds = np.unique(loc[0])
qq = q_inds[-34]



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
a = scorpy.AlgoHandler(blqq_data, sphv_supp, lossy_sphv=True, lossy_iqlm=True, rcond=1e-15)




s1 = scorpy.SphericalVol(path=f'{scorpy.DATADIR}/algo/HIO_ER_test/sphv_HIO_ER_test_200.dbin')
s2 = scorpy.SphericalVol(path=f'{scorpy.DATADIR}/algo/HIO_ER_test/sphv_HIO_ER_test_190.dbin')
s3 = scorpy.SphericalVol(path=f'{scorpy.DATADIR}/algo/HIO_ER_test/sphv_HIO_ER_test_210.dbin')


s1.plot_slice(0, qq)
s2.plot_slice(0, qq)
s3.plot_slice(0, qq)


plt.show()



