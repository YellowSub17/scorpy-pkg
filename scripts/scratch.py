
import numpy as np
np.random.seed(0)
import pyshtools as pysh
import matplotlib.pyplot as plt
plt.close('all')

import scorpy




nq = 45
nphi = 180
ntheta = 90
nl = int(ntheta/2)
qmax= 1
n_harms = 2
lmax = 20


qs=18##working
qs=15 #notworking

# initialize spherical volume and Iqlm handler
sphv1 = scorpy.SphericalVol(nq,ntheta, nphi, qmax)
iqlm = scorpy.IqlmHandler(nq, nl, qmax)

# fill each q shell with n_harm harmonics
print('Spherical Harmonics')
for q_ind in range(nq):

    print()
    for _ in range(n_harms):
        cs = np.random.randint(0, 2)
        l = np.random.randint(cs,lmax+1)*2
        m = np.random.randint(cs, l+1)

        if cs == 0:
            print(q_ind, l, f'+{m}')
        else:
            print(q_ind, l, f'-{m}')
        iqlm.vals[q_ind, cs, l, m] += 1


sphv1.fill_from_iqlm(iqlm)



# get the harmonic order matrix
blqq = scorpy.BlqqVol(nq, nl, qmax)
blqq.fill_from_iqlm(iqlm)

# get eigenvalues and vectors
lams, us = blqq.get_eig()

# knlm -> iqlm prime calculation
knlm = iqlm.copy()
knlm.fill_knlm(us)
iqlmp = knlm.copy()
iqlmp.fill_iqlm_prime(us)



# replot harmonics on new spherical volume
sphv2 = scorpy.SphericalVol(nq,ntheta, nphi, qmax)
sphv2.fill_from_iqlm(iqlmp)


fig, axes = plt.subplots(1,2)
plt.suptitle(f'SPHV q={qs} before/after iteration')

sphv1.plot_slice(0,qs, fig=fig, axes=axes[0], title='Before', xlabel='$\\phi$ [rad]', ylabel='$\\theta$ [rad]')

sphv2.plot_slice(0,qs, fig=fig, axes=axes[1], title='After', xlabel='$\\phi$ [rad]', ylabel='$\\theta$ [rad]')




plt.show()
