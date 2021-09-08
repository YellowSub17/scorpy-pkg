

import numpy as np
# np.random.seed(4)
import scorpy

import matplotlib.pyplot as plt
plt.close('all')






nq = 4097
ntheta = 180
nphi = 360
qmax = 1

nl = int(ntheta/2)

harms = scorpy.utils.harmonic_list(nl)

iqlm = scorpy.IqlmHandler(nq, nl, qmax)



print('Filling iqlm')
for q_ind in range(nq):

    for harm in harms[3000:q_ind+3000]:
        iqlm.add_val(q_ind, harm[0], harm[1])
print('Done.')






fig, axes = plt.subplots(3,4)
for i, q_ind in enumerate([2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096]):
    iqlm.plot_q(q_ind,title=f'{q_ind}', fig=fig, axes=axes.flatten()[i], extent=[-iqlm.nl, iqlm.nl, 0,  iqlm.nl])

fig, axes = plt.subplots(2,3)
for i, l_ind in enumerate([5, 10, 15, 20, 25, 30]):
    iqlm.plot_l(l_ind,title=f'{l_ind}', fig=fig, axes=axes.flatten()[i], extent=[-iqlm.nl,  iqlm.nl, 0, iqlm.qmax])







sphv = scorpy.SphericalVol(nq, ntheta, nphi, qmax)
sphv.fill_from_iqlm(iqlm)

fig, axes = plt.subplots(3,4)
for i, q_ind in enumerate([2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096]):
    sphv.plot_slice(0,q_ind, title=f'{q_ind}', fig=fig, axes=axes.flatten()[i])




iqlmp = iqlm.copy()
iqlmp.fill_from_sphv(sphv)




plt.show()



