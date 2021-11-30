#!/usr/bin/env python3

import scorpy
import numpy as np
import matplotlib.pyplot as plt
import time
import os
plt.close('all')




np.random.seed(1)

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


# a.sphv_iter.save(f'{scorpy.DATADIR}/algo/x.dbin')

a.sphv_iter = scorpy.SphericalVol(path=f'{scorpy.DATADIR}/algo.bkup/HIO_ER_fcc_a/sphv_HIO_ER_fcc_a_0.dbin')



for i in range(5):
    _, _, err = a.HIO()
    print('hio', err)
    a.sphv_iter.plot_slice(0, qq)

_, _, err = a.ER()
print('er', err)
a.sphv_iter.plot_slice(0, qq)

_, _, err = a.ER()
print('er', err)
a.sphv_iter.plot_slice(0, qq)


# s1 = scorpy.SphericalVol(path='/home/pat/Documents/cloudstor/phd/python_projects/scorpy-pkg/data/algo/working_hio/HIO_ER_fcc_a/sphv_HIO_ER_fcc_a_0.dbin')
# s2 = scorpy.SphericalVol(path='/home/pat/Documents/cloudstor/phd/python_projects/scorpy-pkg/data/algo/working_hio/HIO_ER_fcc_b/sphv_HIO_ER_fcc_b_0.dbin')
# s1.plot_slice(0, qq)
# s2.plot_slice(0, qq)
plt.show()


