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









tag = 'ER_rand_a'


sphv_targ = scorpy.SphericalVol(path=f'{scorpy.DATADIR}/algo/{tag}/sphv_{tag}_targ.dbin')
sphv_supp = scorpy.SphericalVol(path=f'{scorpy.DATADIR}/algo/{tag}/sphv_{tag}_supp.dbin')

s = scorpy.SphericalVol(path=f'{scorpy.DATADIR}/algo/{tag}/sphv_{tag}_400.dbin')



loc = np.where(sphv_targ.vol>0)
q_inds = np.unique(loc[0])
qq = q_inds[-4]



sphv_targ.plot_slice(0, qq)
s.plot_slice(0, qq)


# cif1 =  scorpy.CifData(path=f'{scorpy.DATADIR}/cifs/fcc-rand-sf.cif', qmax=89)
# cif2 =  scorpy.CifData(path=f'{scorpy.DATADIR}/cifs/fcc-sf.cif', qmax=89)
# sphv_x = scorpy.SphericalVol(200, 180, 360, 89)
# sphv_x.fill_from_cif(cif1)

# sphv_x.plot_slice(0, qq)









# vals = np.unique(s.vol)
# vals = vals[vals>0]
# plt.figure()
# plt.hist(vals, bins=100)








# y = np.loadtxt(f'{scorpy.DATADIR}/algo/{tag}/errs_{tag}.log', delimiter=',', skiprows=0, usecols=0)

# plt.figure()
# plt.plot(y)


# def sumsquarediff(s1, s2):

    # e = s1.copy()

    # e.vol = s2.vol - s1.vol

    # e.vol = e.vol**2

    # diff = e.vol.sum()
    # diff *= 1/np.sqrt(np.sum(s1.vol**2))
    # diff *= 1/np.sqrt(np.sum(s2.vol**2))

    # return diff















plt.show()
