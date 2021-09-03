

import numpy as np
np.random.seed(4)
import scorpy

import matplotlib.pyplot as plt






nq = 4
ntheta = 180
nphi = 360
qmax = 1

nl = int(ntheta/2)



iqlm = scorpy.IqlmHandler(nq, nl, qmax)




iqlm.vals[0, 0, 5, 3] += 1

iqlm.vals[1, 1, 7, 5] += 1

iqlm.vals[2, 0, 3, 1] += 1
iqlm.vals[2, 1, 1, 1] += 1

iqlm.vals[3] = np.random.random( (2, nl,nl))
iqlm.vals[3, :, 100:, :] *=0



sphv = scorpy.SphericalVol(nq, ntheta, nphi, qmax)
sphv.fill_from_iqlm(iqlm)


fig, axes = plt.subplots(2,2, sharex=True, sharey=True)

sphv.plot_slice(0,0, fig=fig, axes=axes[0,0], title=f'qind=0',  ylabel='$\\theta$')
sphv.plot_slice(0,1, fig=fig, axes=axes[0,1], title=f'qind=1')
sphv.plot_slice(0,2, fig=fig, axes=axes[1,0], title=f'qind=2', xlabel='$\\phi$', ylabel='$\\theta$')
sphv.plot_slice(0,3, fig=fig, axes=axes[1,1], title=f'qind=3', xlabel='$\\phi$')




plt.show()
