
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




sphv = scorpy.SphericalVol(10, 180, 360,1)

# sphv.vol = np.random.random(sphv.vol.shape)
iqlm = scorpy.IqlmHandler(sphv.nl, sphv.nq, sphv.qmax)


im = np.zeros( (sphv.ntheta, sphv.nphi))




xx,yy = np.meshgrid(np.linspace(0, 2*np.pi, sphv.nphi),
                    np.linspace(0, np.pi, sphv.ntheta))


im = np.sin(xx)+np.cos(yy)





sphv.vol[3,...] = np.abs(im)


sphv.plot_slice(0, 3, title='original')




print(iqlm.vals[3])
iqlm.fill_from_sphv(sphv)
print(iqlm.vals[3])




sphv2 = scorpy.SphericalVol(10, 180, 360,1)

sphv2.fill_from_iqlm(iqlm)


sphv2.plot_slice(0, 3, title='from iqlm')









plt.show()
