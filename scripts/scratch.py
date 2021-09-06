
import numpy as np
np.random.seed(0)
import pyshtools as pysh
import matplotlib.pyplot as plt
plt.close('all')

import scorpy



nl = 50


harms = []
for l in range(0, nl, 2):
    for _, m in zip(range(2*l +1), range(-l, l+1)):
        harms.append((l, m))

nphi = nl*2*2
ntheta = nl*2
qmax= 1
nq = 150

# iqlm = scorpy.IqlmHandler(nq, nl, qmax)
# for q_ind, harm in enumerate(harms):
    # iqlm.set_val(q_ind, harm[0], harm[1])

    # lrand = np.random.randint(0, nl)
    # mrand = np.random.randint(-lrand, lrand+1)
    # iqlm.add_val(q_ind,lrand, mrand)

iqlm = scorpy.IqlmHandler(nq, nl, qmax)
for q_ind in range(nq):
    iqlm.set_val(q_ind, harms[q_ind][0], harms[q_ind][1])







sphv1 = scorpy.SphericalVol(nq,ntheta, nphi, qmax)
sphv1.fill_from_iqlm(iqlm)



# get the harmonic order matrix
blqq = scorpy.BlqqVol(nq, nl, qmax)
blqq.fill_from_iqlm(iqlm, inc_odds=True)

# get eigenvalues and vectors
lams, us = blqq.get_eig()

# knlm -> iqlm prime calculation
knlm = iqlm.copy()
knlm.calc_knlm(us)
iqlmp = knlm.copy()
iqlmp.calc_iqlm_prime(us)



# replot harmonics on new spherical volume
sphv2 = scorpy.SphericalVol(nq,ntheta, nphi, qmax)
sphv2.fill_from_iqlm(iqlmp)


fig, axes = plt.subplots(1,2)


loc = np.where(iqlmp.vals !=0)

sphv1.plot_slice(0, loc[0][0], fig=fig, axes=axes[0])
sphv2.plot_slice(0, loc[0][0], fig=fig, axes=axes[1])


blqq.plot_sumax(2)





plt.show()
