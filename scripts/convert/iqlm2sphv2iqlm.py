

import numpy as np
import random
import scorpy

import matplotlib.pyplot as plt
plt.close('all')






nq = 100
ntheta = 180
nphi = 360
qmax = 1

nl = int(ntheta/2)


harms = scorpy.utils.harmonic_list(nl)

iqlm1 = scorpy.IqlmHandler(nq, nl, qmax)

for q_ind in range(nq):
    for _ in range(3):
        harm = random.choice(harms)
        iqlm1.add_val(q_ind, harm[0], harm[1])










sphv1 = scorpy.SphericalVol(nq, ntheta, nphi, qmax)
sphv1.fill_from_iqlm(iqlm1)


iqlm2 = iqlm1.copy()
iqlm2.fill_from_sphv(sphv1)


sphv2 = scorpy.SphericalVol(nq, ntheta, nphi, qmax)
sphv2.fill_from_iqlm(iqlm2)


iqlm3 = iqlm1.copy()
iqlm3.fill_from_sphv(sphv2)


sphv3 = scorpy.SphericalVol(nq, ntheta, nphi, qmax)
sphv3.fill_from_iqlm(iqlm3)



fig, axes = plt.subplots(1,3)
iqlm1.plot_q(5, fig=fig, axes=axes[0], title='iqlm1')
iqlm2.plot_q(5, fig=fig, axes=axes[1], title='iqlm2')
iqlm3.plot_q(5, fig=fig, axes=axes[2], title='iqlm3')


fig, axes = plt.subplots(1,3)
sphv1.plot_slice(0,5, fig=fig, axes=axes[0], title='sphv1')
sphv2.plot_slice(0,5, fig=fig, axes=axes[1], title='sphv2')
sphv3.plot_slice(0,5, fig=fig, axes=axes[2], title='sphv3')



plt.show()



