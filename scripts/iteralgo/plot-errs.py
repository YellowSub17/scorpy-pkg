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
cif_supp = scorpy.CifData(f'{scorpy.DATADIR}/cifs/fcc-sf.cif', qmax = qmax)
sphv_supp = scorpy.SphericalVol(nq, ntheta, nphi, qmax)
sphv_supp.fill_from_cif(cif_supp)
sphv_supp.make_mask()








tag = 'ER_rand_a'

y = np.loadtxt(f'{scorpy.DATADIR}/algo/{tag}/errs_{tag}.log', delimiter=',', skiprows=0, usecols=0)

plt.figure()
plt.plot(y)


# def sumsquarediff(s1, s2):

    # e = s1.copy()

    # e.vol = s2.vol - s1.vol

    # e.vol = e.vol**2

    # diff = e.vol.sum()
    # diff *= 1/np.sqrt(np.sum(s1.vol**2))
    # diff *= 1/np.sqrt(np.sum(s2.vol**2))

    # return diff











s = scorpy.SphericalVol(path=f'{scorpy.DATADIR}/algo/{tag}/sphv_{tag}_150.dbin')
vals = np.unique(s.vol)
vals = vals[vals>0]
plt.figure()
plt.hist(vals, bins=1000)





# qq +=1
# fig, axes = plt.subplots(1,3, sharex=True, sharey=True)
# s.plot_slice(0, qq, fig=fig, axes=axes[0], title='iter')
# sphv_targ.plot_slice(0, qq, fig=fig, axes=axes[1], title='target')
# sphv_supp.plot_slice(0, qq, fig=fig, axes=axes[2], title='supp')




plt.show()
