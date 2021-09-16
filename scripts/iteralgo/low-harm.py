
import numpy as np
np.random.seed(0)
import random
import pyshtools as pysh
import matplotlib.pyplot as plt
plt.close('all')

import scorpy

nq =  100
nphi = 360
ntheta = 180
npsi = 180
nl = int(ntheta/2)
qmax = 1
qq = 10
lq = 50



harms = scorpy.utils.harmonic_list(nl, inc_odds=True)



iqlm = scorpy.IqlmHandler(nq, nl, qmax)
for q_ind in range(nq):

    for i in range(len(harms)):
        harm = random.choice(harms)
        harm = harms[i]
        iqlm.add_val(q_ind, harm[0], harm[1], random.randint(-100, 100))


   #  for harm_ind in range(2556):
        # harm = harms[harm_ind]
        # iqlm.add_val(q_ind, harm[0], harm[1], random.randint(1, 1))

    # harm = harms[q_ind+1000]
    # iqlm.add_val(q_ind, harm[0], harm[1], random.randint(1, 2))








sphv = scorpy.SphericalVol(nq, ntheta, nphi, qmax)
sphv.fill_from_iqlm(iqlm)



blqq = scorpy.BlqqVol(nq, nl, qmax)
blqq.fill_from_iqlm(iqlm)

lams, us = blqq.get_eig()

knlm = iqlm.copy()
knlm.calc_knlm(us)

knlmp = knlm.copy()
# knlmp.calc_knlmp(lams)

iqlmp = knlmp.copy()
iqlmp.calc_iqlmp(us)






sphvp = scorpy.SphericalVol(nq, ntheta, nphi, qmax)
sphvp.fill_from_iqlm(iqlmp)

fig, axes = plt.subplots(1,2, figsize=(8,5), dpi=150, sharey=True)
plt.suptitle('$I(q=10,\\theta, \\phi)$')
sphv.plot_slice(0, qq, fig=fig, axes=axes[0], title='Before', xlabel='$\\phi$ [rad]', ylabel='$\\theta$ [rad]')
sphvp.plot_slice(0,qq, fig=fig, axes=axes[1], title='After',  xlabel='$\\phi$ [rad]',)
plt.savefig('/home/pat/Documents/cloudstor/phd/latex/iteralgo-lowharm/figs/ktrans-sphv.png')


fig, axes = plt.subplots(1,2, figsize=(8,5), dpi=150, sharey=True)
plt.suptitle('$I_{LM}(q=10)$')
iqlm.plot_q(qq, fig=fig, axes=axes[0], title='Before')
iqlmp.plot_q(qq, fig=fig, axes=axes[1], title='After', ylabel='')
plt.savefig('/home/pat/Documents/cloudstor/phd/latex/iteralgo-lowharm/figs/ktrans-lm.png')




fig, axes = plt.subplots(1,2, figsize=(8,5), dpi=150, sharey=True)
plt.suptitle('$I_{L=10,M}(q)$')
iqlm.plot_l(lq, fig=fig, axes=axes[0],title='Before')
iqlmp.plot_l(lq, fig=fig, axes=axes[1],title='After', ylabel='')
plt.savefig('/home/pat/Documents/cloudstor/phd/latex/iteralgo-lowharm/figs/ktrans-mq.png')



plt.figure()
plt.plot(iqlm.vals[qq, 0, :, 0], label='Before')
plt.plot(iqlmp.vals[qq, 0, :, 0], label='After')
plt.legend()
plt.xlabel('$L$')
plt.ylabel('$I_{L,0}$')
plt.title('$I_{L,0}(q=10)$')
plt.savefig('/home/pat/Documents/cloudstor/phd/latex/iteralgo-lowharm/figs/ktrans-lq.png')









plt.show()

