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


np.random.seed(0)



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
a = scorpy.AlgoHandler(blqq_data, sphv_supp, lossy_sphv=True, lossy_iqlm=True, rcond=1e-15)



sphv_init = scorpy.SphericalVol(path=f'{scorpy.DATADIR}/algo/HIO_ER_x3/sphv_iter_HIO_200_ER_200.dbin')
a.sphv_iter = sphv_init.copy()


print(time.asctime())

for i in range(201, 1000):
    stem = f'sphv_iter_HIO_200_ER_{i}'
    print(i, end='\r')
    if i%10==0:
        a.sphv_iter.save(f'{scorpy.DATADIR}/algo/{stem}.dbin')

    _, _, err = a.ER()

    errs_file = open(f'{scorpy.DATADIR}/algo/errs_HIO_200_ER_1000.log', 'a')
    errs_file.write(f'{err},\t\t#{stem}\n')
    errs_file.close()

a.sphv_iter.save(f'{scorpy.DATADIR}/algo/sphv_iter_HIO_200_ER_1000.dbin')

print(time.asctime())











