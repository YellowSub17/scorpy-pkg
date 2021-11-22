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
l_errs = []
ave_diffs = []
std_diffs = []


fnames = []



e = scorpy.SphericalVol(nq, ntheta, nphi, qmax)

for i, fname in enumerate(fnames):
    print(fname)
    s = scorpy.SphericalVol(path=f'{scorpy.DATADIR}/algo/{fname}')
    e.vol = sphv_targ.vol - s.vol

    ave_diffs.append(e.vol[a.supp_loc].mean())
    ave_diffs.append(e.vol[a.supp_loc].mean())
    std_diffs.append(e.vol[a.supp_loc].std())


    e.vol *= e.vol

    t_err = e.vol.sum()
    t_err *= 1/ np.sqrt( np.sum(s.vol * s.vol))
    t_err *= 1/ np.sqrt( np.sum(sphv_targ.vol * sphv_targ.vol))

    t_errs.append(t_err)

    if i > 1:
        s2 = scorpy.SphericalVol(path=f'{scorpy.DATADIR}/algo/{fnames[i-1]}')

        e.vol = s.vol - s2.vol
        e.vol *= e.vol

        l_err = e.vol.sum()
        l_err *= 1/ np.sqrt( np.sum(s.vol * s.vol))
        l_err *= 1/ np.sqrt( np.sum(s2.vol * s2.vol))

        l_errs.append(l_err)



ns = np.arange(0, 201, 10)

start, stop = 0, 20


plt.figure()
plt.plot(ns[start:stop], t_errs[start:stop])
plt.xlabel('n')
plt.ylabel('$\\frac{\\sum (I_{targ} - I_n)^2}{\\sqrt{\\sum I_{targ}^2}\\sqrt{\\sum I_n^2}}$')
plt.title('target error')

plt.figure()
plt.errorbar(ns[start:stop] , ave_diffs[start:stop], yerr=std_diffs[start:stop])
plt.xlabel('n')
plt.ylabel('Average difference from Target')
plt.title('target difference')

plt.figure()
plt.plot(ns[start+1:stop], l_errs[start:stop])
plt.xlabel('n')
plt.ylabel('$\\frac{\\sum (I_{n} - I_{n-10})^2}{\\sqrt{\\sum I_{n-10}^2}\\sqrt{I_n^2}}$')
plt.title('lagging error')











plt.show()







