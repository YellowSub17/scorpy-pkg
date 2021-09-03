
import numpy as np
np.random.seed(0)
import pyshtools as pysh
import matplotlib.pyplot as plt
plt.close('all')

import scorpy




nq = 25
nphi = 180
ntheta = 90
nl = int(ntheta/2)
qmax= 1
n_harms = 3
lmax = 6
qs = 12




# sphv = scorpy.SphericalVol(nq,ntheta, nphi, qmax)

# sphv.vol[0, 45,45] =1
# sphv.vol[0, 60,105] =1
# sphv.plot_slice(0,0)

# iqlm = scorpy.IqlmHandler(nq, nl, qmax)

# iqlm.fill_from_sphv(sphv)
# iqlm.mask_ilm(35)
# iqlm.mask_ilm(lstep=3)



# sphv.fill_from_iqlm(iqlm)

# sphv.plot_slice(0,0)












sphv = scorpy.SphericalVol(nq,ntheta, nphi, qmax)
nl = sphv.nl

iqlm = scorpy.IqlmHandler(nq, nl, qmax)

for q_ind in range(nq):
    for _ in range(n_harms):
        cs = np.random.randint(0, 2)
        l = np.random.randint(cs,lmax+1)
        m = np.random.randint(cs, l+1)

        if cs == 0:
            print(q_ind, l, f'+{m}')
        else:
            print(q_ind, l, f'-{m}')


        iqlm.vals[q_ind][cs, l, m] += 1




sphv.fill_from_iqlm(iqlm)

sphv.plot_slice(0,qs)







blqq = scorpy.BlqqVol(nq, nl, qmax)

blqq.fill_from_iqlm(iqlm)

# blqq.plot_slice(2,4)




lams, us = blqq.get_eig()




knlm = iqlm.copy()
knlm.fill_knlm(us)



iqlmp = knlm.copy()
iqlmp.fill_iqlm_prime(us)



sphv.fill_from_iqlm(iqlmp)

sphv.plot_slice(0,qs)
















plt.show()
