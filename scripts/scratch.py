
import numpy as np
import pyshtools as pysh
import matplotlib.pyplot as plt
plt.close('all')

import scorpy




nq = 1
nphi = 360*5
ntheta = 180*5
qmax= 1




sphv = scorpy.SphericalVol(nq, ntheta, nphi, qmax)



for i in range(3):
    x = np.random.randint(0, nphi)
    y = np.random.randint(0, ntheta)
    sphv.vol[0, y,x] = 1

sphv.plot_slice(0,0, cmap='bone')

iqlm = scorpy.IqlmHandler(nq, sphv.nl, qmax)


iqlm.fill_from_sphv(sphv)

iqlm.mask_ilm(0,54)

sphv.fill_from_iqlm(iqlm)

sphv.plot_slice(0,0, cmap='bone')

iqlm.mask_ilm(0,54, 6)

sphv.fill_from_iqlm(iqlm)

sphv.plot_slice(0,0, cmap='Dark2')



plt.show()
