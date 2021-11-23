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

y1 = np.loadtxt(f'{scorpy.DATADIR}/algo/x/errs_HIO_200.log', delimiter=',', skiprows=0, usecols=0)
y2 = np.loadtxt(f'{scorpy.DATADIR}/algo/x/errs_HIO_200_ER_200.log', delimiter=',', skiprows=0, usecols=0)
y3 = np.loadtxt(f'{scorpy.DATADIR}/algo/x/errs_HIO_200_ER_200_HIO_200.log', delimiter=',', skiprows=0, usecols=0)
y4 = np.loadtxt(f'{scorpy.DATADIR}/algo/x/errs_HIO_200_ER_200_HIO_200_ER_200.log', delimiter=',', skiprows=0, usecols=0)
y5 = np.loadtxt(f'{scorpy.DATADIR}/algo/x/errs_HIO_200_ER_200_x2_HIO_200.log', delimiter=',', skiprows=0, usecols=0)
y6 = np.loadtxt(f'{scorpy.DATADIR}/algo/x/errs_HIO_200_ER_200_x2_HIO_200_ER_200.log', delimiter=',', skiprows=0, usecols=0)

y = list(y1[1:]) + list(y2) + list(y3) + list(y4[1:]) + list(y5) + list(y6[1:])
plt.figure()
plt.plot(y)



y = y[300:]
plt.figure()
plt.plot(y)

y = y[400:]
plt.figure()
plt.plot(y)

y = y[298:]
plt.figure()
plt.plot(y)






def sumsquarediff(s1, s2):

    e = s1.copy()

    e.vol = s2.vol - s1.vol

    e.vol = e.vol**2

    diff = e.vol.sum()
    diff *= 1/np.sqrt(np.sum(s1.vol**2))
    diff *= 1/np.sqrt(np.sum(s2.vol**2))

    return diff



stems = []

for i in range(0, 201, 10):
    stems.append(f'sphv_iter_HIO_{i}')

for i in range(10, 201, 10):
    stems.append(f'sphv_iter_HIO_200_ER_{i}')

for i in range(10, 201, 10):
    stems.append(f'sphv_iter_HIO_200_ER_200_HIO_{i}')

for i in range(10, 201, 10):
    stems.append(f'sphv_iter_HIO_200_ER_200_HIO_200_ER_{i}')

for i in range(10, 201, 10):
    stems.append(f'sphv_iter_HIO_200_ER_200_x2_HIO_{i}')

for i in range(10, 201, 10):
    stems.append(f'sphv_iter_HIO_200_ER_200_x2_HIO_200_ER_{i}')


diffs = []
for stem in stems:
    print(stem)
    # assert Path(f'{scorpy.DATADIR}/algo/x/{stem}.dbin').is_file(), f'path={scorpy.DATADIR}/algo/x/{stem}.dbin not found'
    s = scorpy.SphericalVol(path=f'{scorpy.DATADIR}/algo/x/{stem}.dbin')
    diff = sumsquarediff(sphv_targ, s)
    diffs.append(diff)

plt.figure()
plt.plot(diffs)

plt.show()










# plt.figure()
# s = scorpy.SphericalVol(path=f'{scorpy.DATADIR}/algo/x/sphv_iter_HIO_200_ER_200.dbin')
# vals = np.unique(s.vol)
# vals = vals[vals>0]
# plt.hist(vals, bins=1000)
# sumsquarediff(s)


# s = scorpy.SphericalVol(path=f'{scorpy.DATADIR}/algo/x/sphv_iter_HIO_200_ER_200_HIO_200_ER_200.dbin')
# vals = np.unique(s.vol)
# vals = vals[vals>0]
# plt.hist(vals, bins=1000)
# sumsquarediff(s)

# s = scorpy.SphericalVol(path=f'{scorpy.DATADIR}/algo/sphv_iter_HIO_200_ER_200_x2_HIO_200_ER_200.dbin')
# vals = np.unique(s.vol)
# vals = vals[vals>0]
# plt.hist(vals, bins=1000)
# sumsquarediff(s)




plt.show()
