
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


qmax = 40
# qmax = 1.5

lq = 60
qq = 92


cif = scorpy.CifData(f'{scorpy.DATADIR}/cifs/fcc-sf.cif', qmax=qmax)
sphv = scorpy.SphericalVol(nq, ntheta, nphi, qmax)
sphv.fill_from_cif(cif)
sphv.plot_slice(0, qq, title='From CIF')



# corr = scorpy.CorrelationVol(nq, npsi, qmax)
# corr.fill_from_cif(cif)
# corr.plot_q1q2()
# blqq = scorpy.BlqqVol(nq, nl, qmax)
# blqq.fill_from_corr(corr)
# blqq.plot_q1q2()
# lams, us = blqq.get_eig()
# lams, us = np.real(lams), np.real(us)


iqlm = scorpy.IqlmHandler(nq, nl, qmax)
iqlm.fill_from_sphv(sphv)
blqq = scorpy.BlqqVol(nq, nl, qmax)
blqq.fill_from_iqlm(iqlm)
lams, us = blqq.get_eig()
lams, us = np.real(lams), np.real(us)



iqlm = scorpy.IqlmHandler(nq, nl, qmax)
iqlm.fill_from_sphv(sphv)
knlm = iqlm.copy()
knlm.calc_knlm(us)
knlmp = knlm.copy()
knlmp.calc_knlmp(lams)
iqlmp = knlmp.copy()
iqlmp.calc_iqlmp(us)



fig, axes = plt.subplots(1,2, sharex=True, sharey=True)
iqlm.plot_q(qq, fig=fig, axes=axes[0], title='Initial')
iqlmp.plot_q(qq, fig=fig, axes=axes[1], title='Final')


plt.show()

