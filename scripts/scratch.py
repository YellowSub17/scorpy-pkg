
import numpy as np
import pyshtools as pysh
import matplotlib.pyplot as plt
plt.close('all')

import scorpy






# v = scorpy.Vol(10,10,10, 0,0,0, 1,1,1)
# v.vol = np.random.random(v.vol.shape)


# fig, axes = plt.subplots(2,2, figsize=(5,5),dpi=150,  sharey=True, sharex=True)

# v.plot_xy(fig=fig, axes=axes[0,0])
# v.plot_sumax(1, fig=fig, axes=axes[0,1], title='Yahoo!')
# v.plot_sumax(1, fig=fig, axes=axes[1,0], vminmax=(None, 4), ylabel='apple')
# v.plot_sumax(1, fig=fig, axes=axes[1,1], vminmax=(6,None), xlabel='orange')




nq = 1
nphi = 360
ntheta = 180
qmax= 1




sphv = scorpy.SphericalVol(nq, ntheta, nphi, qmax)

iqlm = scorpy.IqlmHandler(nq, sphv.nl, qmax) 



iqlm.vals[0][0,5,4] = 1
iqlm.vals[0][1,6,4] = 1


sphv.fill_from_iqlm(iqlm)
sphv.plot_slice(0,0, cmap='Dark2')


iqlm.mask_ilm(6, 7)

sphv.fill_from_iqlm(iqlm)
sphv.plot_slice(0,0, cmap='Dark2')




# iqlm




plt.show()
