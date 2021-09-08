

import numpy as np
# np.random.seed(4)
import scorpy

import matplotlib.pyplot as plt






nq = 150
ntheta = 180
nphi = 360
qmax = 1

nl = int(ntheta/2)

harms = scorpy.utils.harmonic_list(nl)



iqlm = scorpy.IqlmHandler(nq, nl, qmax)


# for q_ind in range(nq):
    # lm_ind = np.random.randint(0,len(harms))
    # lm = harms[lm_ind]
    # print(lm)
    # iqlm.add_val(q_ind, lm[0], lm[1])

for q_ind in range(nq):

    iqlm.add_val(q_ind, harms[q_ind][0], harms[q_ind][1]) 






sphv = scorpy.SphericalVol(nq, ntheta, nphi, qmax)
sphv.fill_from_iqlm(iqlm)


fig, axes = plt.subplots(2,2)

sphv.plot_slice(0,0, fig=fig, axes=axes[0,0], title=f'qind=0')
sphv.plot_slice(0,1, fig=fig, axes=axes[0,1], title=f'qind=1')
sphv.plot_slice(0,2, fig=fig, axes=axes[1,0], title=f'qind=2')
sphv.plot_slice(0,3, fig=fig, axes=axes[1,1], title=f'qind=3')




iqlmp = iqlm.copy()

iqlmp.vals *=0

iqlmp.fill_from_sphv(sphv)



iqlm.plot_qharms(-1)

iqlm.plot_lq(12)








plt.show()
