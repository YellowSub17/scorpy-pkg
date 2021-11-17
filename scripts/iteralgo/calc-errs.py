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




t_errs = []
n_errs = []
ave_diffs = []
std_diffs = []


fnames = []

for i in range(0, 401, 10):
    fnames.append(f'sphv_iter_ER_{i}')

for i in range(0, 201, 10):
    fnames.append(f'sphv_iter_ER_400_HIO_{i}')

for i in range(0, 201, 10):
    fnames.append(f'sphv_iter_ER_400_HIO_200_ER_{i}')


for i, fname in enumerate(fnames[1:]):
    print(fname)
    s = scorpy.SphericalVol(path=f'{scorpy.DATADIR}/algo/ER/{fname}')
    e = sphv_targ.copy()
    e.vol -=s.vol

    ave_diffs.append(e.vol[a.supp_loc].mean())
    std_diffs.append(e.vol[a.supp_loc].std())

    e.vol *= e.vol

    t_err = e.vol.sum()
    t_err *= 1/ np.sqrt( np.sum(s.vol * s.vol))
    t_err *= 1/ np.sqrt( np.sum(sphv_targ.vol * sphv_targ.vol))

    t_errs.append(t_err)

    if i > 1:
        s1 = scorpy.SphericalVol(path=f'{scorpy.DATADIR}/algo/ER/{fname}')
        s2 = scorpy.SphericalVol(path=f'{scorpy.DATADIR}/algo/ER/{fnames[i-1]}')

        s2.vol -= s1.vol
        s2.vol *= s2.vol

        n_err = s2.vol.sum()
        n_err *= 1/ np.sqrt( np.sum(s1.vol * s1.vol))
        n_err *= 1/ np.sqrt( np.sum(s2.vol * s2.vol))

        n_errs.append(n_err)




plt.figure()
plt.plot(t_errs)
plt.xlabel('n')
plt.ylabel('$\\frac{\\sum (I_{targ} - I_n)^2}{\\sqrt{\\sum I_{targ}^2}\\sqrt{\\sum I_n^2}}$')
plt.title('400 ER 200 HIO')

plt.figure()
plt.errorbar(list(range(len(ave_diffs))), ave_diffs, yerr=std_diffs)
plt.xlabel('n')
plt.ylabel('Average difference from Target')
plt.title('400 ER 200 HIO')

plt.figure()
plt.plot(n_errs)
plt.xlabel('n')
plt.ylabel('$\\frac{\\sum (I_{n} - I_{n-10})^2}{\\sqrt{\\sum I_{n-10}^2}\\sqrt{I_n^2}}$')
plt.title('400 ER 200 HIO')






fig, axes = plt.subplots(2,2, sharex=True, sharey=True)

sphv_targ.plot_slice(0, 34, fig=fig, axes=axes[0,0], title='targ')

s = scorpy.SphericalVol(path=f'{scorpy.DATADIR}/algo/ER/sphv_iter_ER_400')
s.plot_slice(0, 34, fig=fig, axes=axes[0,1], title='ER 400')

s = scorpy.SphericalVol(path=f'{scorpy.DATADIR}/algo/ER/sphv_iter_ER_400_HIO_200')
s.plot_slice(0, 34, fig=fig, axes=axes[1,0], title='ER 400 HIO 200')

s = scorpy.SphericalVol(path=f'{scorpy.DATADIR}/algo/ER/sphv_iter_ER_400_HIO_200_ER_200')
s.plot_slice(0, 34, fig=fig, axes=axes[1,1], title='ER 400 HIO 200 ER 200')






fig, axes = plt.subplots(1,2, sharex=True, sharey=True)


s = scorpy.SphericalVol(path=f'{scorpy.DATADIR}/algo/ER/sphv_iter_ER_400')
s.plot_slice(0, 34, fig=fig, axes=axes[0], title='')

s = scorpy.SphericalVol(path=f'{scorpy.DATADIR}/algo/ER/sphv_iter_ER_400_HIO_0')
s.plot_slice(0, 34, fig=fig, axes=axes[1], title='')





plt.show()







