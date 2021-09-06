import numpy as np
import scorpy
import matplotlib.pyplot as plt
plt.close('all')








nq = 1
ntheta = 180
nphi = 360
qmax = 1


nl = int(ntheta/2)






sphv = scorpy.SphericalVol(nq, ntheta, nphi, qmax)


for _ in range(10):
    x = np.random.randint(0, nphi)
    y = np.random.randint(0, ntheta)

    sphv.vol[0,y,x] = 1


sphv.plot_slice(0,0)



iqlm = scorpy.IqlmHandler(nq, nl, qmax)

iqlm.fill_from_sphv(sphv)
sphv.fill_from_iqlm(iqlm)
sphv.plot_slice(0,0)

sphv.plot_slice(0,0, cmap='Dark2')



plt.show()
