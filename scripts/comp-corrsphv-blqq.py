



import scorpy

import numpy as np

import matplotlib.pyplot as plt



nq = 100
npsi = 180


nl = 90
ntheta = 2*nl
nphi = 2*ntheta

qmax = 1



cif = scorpy.CifData(f'{scorpy.DATADIR}/cifs/1al1-sf.cif', qmax=qmax)


# corr = scorpy.CorrelationVol(nq, npsi, qmax)
# corr.fill_from_cif(cif)
# corr.save(f'{scorpy.DATADIR}/dbins/x')


corr = scorpy.CorrelationVol(path=f'{scorpy.DATADIR}/dbins/x')


sphv  = scorpy.SphericalVol(nq, ntheta, nphi, qmax)
sphv.fill_from_cif(cif)
iqlm = scorpy.IqlmHandler(nq, nl, qmax)
iqlm.fill_from_sphv(sphv)


blqq1 = scorpy.BlqqVol(nq, nl, qmax)
blqq1.fill_from_corr(corr, inc_odds=False, rcond=1e-1)

blqq2 = scorpy.BlqqVol(nq, nl, qmax)
blqq2.fill_from_iqlm(iqlm, inc_odds=False)





fig, axes = plt.subplots(1,2)
blqq1.plot_q1q2(fig=fig, axes=axes[0])
blqq2.plot_q1q2(fig=fig, axes=axes[1])




lq = 32
fig, axes = plt.subplots(1,2)
blqq1.plot_slice(2, lq, fig=fig, axes=axes[0])
blqq2.plot_slice(2, lq, fig=fig, axes=axes[1])
plt.show()












