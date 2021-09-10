
import numpy as np
np.random.seed(0)
import random
import pyshtools as pysh
import matplotlib.pyplot as plt
plt.close('all')

import scorpy



nl = 50

harms = scorpy.utils.harmonic_list(nl)

nphi = nl*2*2
ntheta = nl*2
qmax= 1
nq = 150



iqlm = scorpy.IqlmHandler(nq, nl, qmax)
# for q_ind in range(nq):
    # iqlm.set_val(q_ind, harms[q_ind][0], harms[q_ind][1])
    # iqlm.set_val(q_ind, harms[q_ind][0]+1, harms[q_ind][1])




# harms = scorpy.utils.harmonic_list(nl)

for q_ind in range(nq):
    for _ in range(100):
        harm = random.choice(harms)
        iqlm.add_val(q_ind, harm[0], harm[1])





sphv1 = scorpy.SphericalVol(nq,ntheta, nphi, qmax)
sphv1.fill_from_iqlm(iqlm)


# get the harmonic order matrix
blqq = scorpy.BlqqVol(nq, nl, qmax)
blqq.fill_from_iqlm(iqlm, inc_odds=True)

# get eigenvalues and vectors
lams, us = blqq.get_eig(herm=True)



# knlm -> iqlm prime calculation
knlm = iqlm.copy()
knlm.calc_knlm(us)

knlm_loc = np.where(knlm.vals != 0)





knlmp = knlm.copy()
knlmp.calc_knlmp(lams)


iqlmp = knlmp.copy()
iqlmp.calc_iqlmp(us)

iqlmp_loc = np.where(iqlmp.vals != 0)



# replot harmonics on new spherical volume
sphv2 = scorpy.SphericalVol(nq,ntheta, nphi, qmax)
sphv2.fill_from_iqlm(iqlmp)

sphv_diff = sphv2.copy()
sphv_diff.vol -= sphv1.vol


qs = [40]
for q_ind in qs:
    fig, axes = plt.subplots(1,3)
    plt.suptitle(f'q shell {q_ind}')
    sphv1.plot_slice(0, q_ind, fig=fig, axes=axes[0], title='Before')
    sphv2.plot_slice(0, q_ind, fig=fig, axes=axes[1], title='After')
    sphv_diff.plot_slice(0, q_ind, fig=fig, axes=axes[2], title='Difference')






plt.show()
