
import numpy as np
np.random.seed(0)
import random
import pyshtools as pysh
import matplotlib.pyplot as plt
plt.close('all')

import scorpy

nq = 100
nphi = 360
ntheta = 180
npsi = 180
nl = int(ntheta/2)
qmax = 1
qq = 70



harms = scorpy.utils.harmonic_list(nl, inc_odds=False)



iqlm = scorpy.IqlmHandler(nq, nl, qmax)
for q_ind in range(nq):

    # for _ in range(1000):
        # harm = random.choice(harms)
        # iqlm.add_val(q_ind, harm[0], harm[1], random.randint(1, 10))



    for harm_ind in range(2000):
        harm = harms[harm_ind]
        iqlm.add_val(q_ind, harm[0], harm[1], random.randint(1, 2))

    harm = harms[q_ind+1000]
    iqlm.add_val(q_ind, harm[0], harm[1], random.randint(1, 10))


iqlm.plot_q(qq)






sphv = scorpy.SphericalVol(nq, ntheta, nphi, qmax)
sphv.fill_from_iqlm(iqlm)


sphv.plot_slice(0, qq)

blqq = scorpy.BlqqVol(nq, nl, qmax)
blqq.fill_from_iqlm(iqlm)

lams, us = blqq.get_eig()

knlm = iqlm.copy()
knlm.calc_knlm(us)

knlmp = knlm.copy()
knlmp.calc_knlmp(lams)

iqlmp = knlmp.copy()
iqlmp.calc_iqlmp(us)

iqlmp.plot_q(qq)




sphvp = scorpy.SphericalVol(nq, ntheta, nphi, qmax)
sphvp.fill_from_iqlm(iqlmp)

sphvp.plot_slice(0,qq)















plt.show()

