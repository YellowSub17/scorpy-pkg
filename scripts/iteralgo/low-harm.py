
import numpy as np
np.random.seed(0)
import random
import pyshtools as pysh
import matplotlib.pyplot as plt
plt.close('all')

import scorpy

nq = 1
# nphi = 40
# ntheta = 20
nphi = 360
ntheta = 180
npsi = 180
nl = int(ntheta/2)
qmax = 1
qq = 0

iqlm = scorpy.IqlmHandler(nq, nl, qmax)

harms = scorpy.utils.harmonic_list(nl, inc_odds=True)
for q_ind in range(nq):
    for harm_ind in range(5393):
        harm = harms[harm_ind]
        iqlm.add_val(q_ind, harm[0], harm[1], random.randint(-10,20))


sphv = scorpy.SphericalVol(nq, ntheta, nphi, qmax)
sphv.fill_from_iqlm(iqlm)
blqq = scorpy.BlqqVol(nq, nl, qmax)
blqq.fill_from_iqlm(iqlm)
lams, us = blqq.get_eig()
knlm = iqlm.copy()
knlm.calc_knlm(us)
knlmp = knlm.copy()
knlmp.calc_knlmp(lams)
iqlmp = knlmp.copy()
iqlmp.calc_iqlmp(us)
sphvp = scorpy.SphericalVol(nq, ntheta, nphi, qmax)
sphvp.fill_from_iqlm(iqlmp)

fig, axes = plt.subplots(1,3, figsize=(8,5), dpi=150, sharey=True, sharex=True)
plt.suptitle(f'$I_{{LM}}$')
iqlm.plot_q(qq, fig=fig, axes=axes[0], title='Initial')
iqlmp.plot_q(qq, fig=fig, axes=axes[1], title='Final', ylabel='')


iqdiv = iqlmp.copy()
loc = np.where(iqdiv.vals != 0)
iqdiv.vals[loc] /= iqlm.vals[loc]

iqdiv.plot_q(qq, fig=fig, axes=axes[2], title='Final/Initial', ylabel='')



# plt.savefig(f'/home/pat/Documents/cloudstor/phd/latex/factors-kprime/figs/no-ldep.png')


plt.show()





# L = np.arange(40)
# plt.figure()
# plt.plot(L, 1/np.sqrt(2*L+1))
# plt.show()
